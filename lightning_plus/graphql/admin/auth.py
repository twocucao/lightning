from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject

from lightning_plus.contrib.exceptions import AuthFailed


def authenticate(request):
    pass


def get_user(request):
    if not hasattr(request, "user"):
        request.user = authenticate(request=request)
    return request.user


def calc_depth(path):
    if not path.prev:
        return 1
    else:
        return calc_depth(path.prev) + 1


allow_list = [
    "login",
    "healthCheck",
]


class AuthMiddleware:
    def resolve(self, next, root, info, **kwargs):
        depth = calc_depth(info.path)
        request = info.context
        if depth == 1:
            request.user = get_user(request)
            if isinstance(request.user, AnonymousUser):
                raise AuthFailed("无法登陆")
            assert request.user
        return next(root, info, **kwargs)
