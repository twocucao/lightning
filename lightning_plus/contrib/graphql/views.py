import json
import logging
import traceback
from typing import Any, Dict, List, Optional, Tuple, Union

import opentracing
import opentracing.tags
from django.conf import settings
from django.db import connection
from django.db.backends.postgresql.base import DatabaseWrapper
from django.http import (
    HttpRequest,
    HttpResponseNotAllowed,
    JsonResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.functional import SimpleLazyObject
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from graphene_django.settings import graphene_settings
from graphene_django.views import instantiate_middleware, HttpError
from graphql import parse, get_operation_ast, OperationType, validate
from graphql.error import (
    GraphQLError,
    format_error as format_graphql_error,
)
from graphql.execution import ExecutionResult
from jwt.exceptions import PyJWTError

from ..exceptions import PermissionDenied

API_PATH = SimpleLazyObject(lambda: reverse("api"))

unhandled_errors_logger = logging.getLogger("saleor.graphql.errors.unhandled")
handled_errors_logger = logging.getLogger("saleor.graphql.errors.handled")


def tracing_wrapper(execute, sql, params, many, context):
    conn: DatabaseWrapper = context["connection"]
    operation = f"{conn.alias} {conn.display_name}"
    with opentracing.global_tracer().start_active_span(operation) as scope:
        span = scope.span
        span.set_tag(opentracing.tags.COMPONENT, "db")
        span.set_tag(opentracing.tags.DATABASE_STATEMENT, sql)
        span.set_tag(opentracing.tags.DATABASE_TYPE, conn.display_name)
        return execute(sql, params, many, context)


class GraphQLView(View):
    # - Playground as default the API explorer
    # - file upload
    # - query batching
    # - CORS

    schema = None
    middleware = None
    root_value = None

    HANDLED_EXCEPTIONS = (GraphQLError, PyJWTError, PermissionDenied)

    def __init__(self, schema, middleware=None, root_value=None):
        super().__init__()
        if middleware is None:
            middleware = graphene_settings.MIDDLEWARE
        self.schema = self.schema or schema
        if middleware is not None:
            self.middleware = list(instantiate_middleware(middleware))
        self.root_value = root_value

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.render_playground(request)
        if request.method == "OPTIONS":
            response = self.options(request, *args, **kwargs)
        elif request.method == "POST":
            response = self.handle_query(request)
        else:
            return HttpResponseNotAllowed(["GET", "OPTIONS", "POST"])
        # Add access control headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response[
            "Access-Control-Allow-Headers"
        ] = "Origin, Content-Type, Accept, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    def render_playground(self, request):
        return render(request, "graphql_playground.html", {})

    def _handle_query(self, request: HttpRequest) -> JsonResponse:
        try:
            data = self.parse_body(request)
        except ValueError:
            return JsonResponse(
                data={"errors": [self.format_error("Unable to parse query.")]},
                status=400,
            )

        if isinstance(data, list):
            responses = [self.get_response(request, entry) for entry in data]
            result: Union[list, Optional[dict]] = [
                response for response, code in responses
            ]
            status_code = max((code for response, code in responses), default=200)
        else:
            result, status_code = self.get_response(request, data)
        return JsonResponse(data=result, status=status_code, safe=False)

    def handle_query(self, request: HttpRequest) -> JsonResponse:
        with opentracing.global_tracer().start_active_span("http") as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "http")
            span.set_tag(opentracing.tags.HTTP_METHOD, request.method)
            span.set_tag(
                opentracing.tags.HTTP_URL,
                request.build_absolute_uri(request.get_full_path()),
            )

            request_ips = request.META.get(settings.REAL_IP_ENVIRON, "")
            for ip in request_ips.split(","):
                span.set_tag(opentracing.tags.PEER_HOST_IPV4, ip)
                span.set_tag("http.client_ip", ip)
                span.set_tag("http.client_ip_originated_from", settings.REAL_IP_ENVIRON)
                break

            response = self._handle_query(request)
            span.set_tag(opentracing.tags.HTTP_STATUS_CODE, response.status_code)

            # RFC2616: Content-Length is defined in bytes,
            # we can calculate the RAW UTF-8 size using the length of
            # response.content of type 'bytes'
            span.set_tag("http.content_length", len(response.content))

            return response

    def get_response(
        self, request: HttpRequest, data: dict
    ) -> Tuple[Optional[Dict[str, List[Any]]], int]:
        query, variables, operation_name = self.get_graphql_params(request, data)
        execution_result = self.execute_graphql_request(
            request, data, query, variables, operation_name
        )
        status_code = 200
        if execution_result:
            response = {}
            if execution_result.errors:
                response["errors"] = [
                    self.format_error(e) for e in execution_result.errors
                ]
            response["data"] = execution_result.data
            result: Optional[Dict[str, List[Any]]] = response
        else:
            result = None

        return result, status_code

    def get_root_value(self, request):
        return self.root_value

    def get_middleware(self, request):
        return self.middleware

    def get_context(self, request):
        return request

    def execute_graphql_request(
        self,
        request,
        data,
        query,
        variables,
        operation_name,
    ):
        if not query:
            raise HttpError(HttpResponseBadRequest("Must provide query string."))
        with opentracing.global_tracer().start_active_span("graphql_query") as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "GraphQL")

            try:
                document = parse(query)
            except GraphQLError as e:
                return ExecutionResult(errors=[e], data=dict(invalid=True))

            if request.method.lower() == "get":
                operation_ast = get_operation_ast(document, operation_name)
                if operation_ast and operation_ast.operation != OperationType.QUERY:
                    raise HttpError(
                        HttpResponseNotAllowed(
                            ["POST"],
                            "Can only perform a {} operation from a POST request.".format(
                                operation_ast.operation.value
                            ),
                        )
                    )

            validation_errors = validate(self.schema.graphql_schema, document)
            if validation_errors:
                return ExecutionResult(data=None, errors=validation_errors)

            try:
                with connection.execute_wrapper(tracing_wrapper):
                    return self.schema.execute(
                        source=query,
                        root_value=self.get_root_value(request),
                        variable_values=variables,
                        operation_name=operation_name,
                        context_value=self.get_context(request),
                        middleware=self.get_middleware(request),
                    )
            except GraphQLError as e:
                span.set_tag(opentracing.tags.ERROR, True)
                return ExecutionResult(errors=[e])

    @staticmethod
    def parse_body(request: HttpRequest):
        content_type = request.content_type
        if content_type == "application/graphql":
            return {"query": request.body.decode("utf-8")}
        if content_type == "application/json":
            body = request.body.decode("utf-8")
            return json.loads(body)
        if content_type in ["application/x-www-form-urlencoded", "multipart/form-data"]:
            return request.POST
        return {}

    @staticmethod
    def get_graphql_params(request: HttpRequest, data: dict):
        query = data.get("query")
        variables = data.get("variables")
        operation_name = data.get("operationName")
        if operation_name == "null":
            operation_name = None

        if request.content_type == "multipart/form-data":
            operations = json.loads(data.get("operations", "{}"))
            files_map = json.loads(data.get("map", "{}"))
            for file_key in files_map:
                # file key is which file it is in the form-data
                file_instances = files_map[file_key]
                for file_instance in file_instances:
                    obj_set(operations, file_instance, file_key, False)
            query = operations.get("query")
            variables = operations.get("variables")
        return query, variables, operation_name

    @classmethod
    def format_error(cls, error):
        if isinstance(error, GraphQLError):
            result = format_graphql_error(error)
        else:
            result = {"message": str(error)}

        exc = error
        while isinstance(exc, GraphQLError) and hasattr(exc, "original_error"):
            exc = exc.original_error

        if isinstance(exc, cls.HANDLED_EXCEPTIONS):
            handled_errors_logger.error("A query had an error", exc_info=exc)
        else:
            unhandled_errors_logger.error("A query failed unexpectedly", exc_info=exc)

        result["extensions"] = {"exception": {"code": type(exc).__name__}}
        if settings.DEBUG:
            lines = []

            if isinstance(exc, BaseException):
                for line in traceback.format_exception(
                    type(exc), exc, exc.__traceback__
                ):
                    lines.extend(line.rstrip().splitlines())
            result["extensions"]["exception"]["stacktrace"] = lines
        return result


def get_key(key):
    try:
        int_key = int(key)
    except (TypeError, ValueError):
        return key
    else:
        return int_key


def get_shallow_property(obj, prop):
    if isinstance(prop, int):
        return obj[prop]
    try:
        return obj.get(prop)
    except AttributeError:
        return None


def obj_set(obj, path, value, do_not_replace):
    if isinstance(path, int):
        path = [path]
    if not path:
        return obj
    if isinstance(path, str):
        new_path = [get_key(part) for part in path.split(".")]
        return obj_set(obj, new_path, value, do_not_replace)

    current_path = path[0]
    current_value = get_shallow_property(obj, current_path)

    if len(path) == 1:
        if current_value is None or not do_not_replace:
            obj[current_path] = value

    if current_value is None:
        try:
            if isinstance(path[1], int):
                obj[current_path] = []
            else:
                obj[current_path] = {}
        except IndexError:
            pass
    return obj_set(obj[current_path], path[1:], value, do_not_replace)
