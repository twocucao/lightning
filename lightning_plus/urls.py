from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views import defaults as default_views

from lightning_plus.puzzle.urls import urlpatterns as puzzle_urls
from lightning_plus.lightning.urls import urlpatterns as lightning_urls

urlpatterns = (
    [
        url(
            r"^api/puzzle/",
            include((puzzle_urls, "puzzle"), namespace="puzzle"),
        ),
        path(
            "",
            include((lightning_urls, "lightning")),
        ),
        url(
            r"^400/$",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        url(
            r"^403/$",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        url(
            r"^404/$",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        url(r"^500/$", default_views.server_error),
    ]  # type: ignore
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
)

admin.site.site_header = "后台"
admin.site.site_title = "后台"
admin.site.index_title = "后台"

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [url(r"^__debug__/", include(debug_toolbar.urls))]
