import opentracing
import opentracing.tags
from django.utils.functional import SimpleLazyObject
from graphql import GraphQLResolveInfo

from .tracing import should_trace
from .views import GraphQLView


def authenticate(request):
    pass


def get_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = authenticate(request=request)
    return request._cached_user


class JWTMiddleware:
    def resolve(self, next, root, info, **kwargs):
        request = info.context
        request.user = SimpleLazyObject(lambda: get_user(request))
        return next(root, info, **kwargs)


class OpentracingGrapheneMiddleware:
    @staticmethod
    def resolve(next_, root, info: GraphQLResolveInfo, **kwargs):
        if not should_trace(info):
            return next_(root, info, **kwargs)
        operation = f"{info.parent_type.name}.{info.field_name}"
        with opentracing.global_tracer().start_active_span(operation) as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "graphql")
            span.set_tag("graphql.parent_type", info.parent_type.name)
            span.set_tag("graphql.field_name", info.field_name)
            return next_(root, info, **kwargs)



