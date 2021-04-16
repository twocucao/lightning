from django.conf import settings
from django.http import HttpRequest, HttpResponse

from lightning_plus.contrib.graphql.views import GraphQLView

allow_headers = [
    "Origin",
    "X-Requested-With",
    "Content-Type",
    "Accept",
    "Authorization",
]


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.process_request(request)
        self.patch_cors_policy(request, response)
        return response

    def patch_cors_policy(self, request, response):
        origin = request.headers.get("origin", None)
        if origin:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
            response["Access-Control-Allow-Headers"] = ",".join(allow_headers)
        else:
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Credentials"] = "true"

    def process_request(self, request):
        if (
                request.method == "OPTIONS"
                and "HTTP_ACCESS_CONTROL_REQUEST_METHOD" in request.META
        ):
            response = HttpResponse()
            response["Content-Length"] = "0"
            return response
        response: HttpResponse = self.get_response(request)
        return response


def process_view(self, request, view_func, *args):
    if hasattr(view_func, "view_class") and issubclass(
            view_func.view_class, GraphQLView
    ):
        request._graphql_view = True


if settings.ENABLE_DEBUG_TOOLBAR:
    import warnings

    try:
        from graphiql_debug_toolbar.middleware import DebugToolbarMiddleware
    except ImportError:
        warnings.warn("The graphiql debug toolbar was not installed.")
    else:
        DebugToolbarMiddleware.process_view = process_view
