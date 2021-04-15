from lightning_plus.api_basebone.drf.routers import SimpleRouter
from .upload import views as upload_views


router = SimpleRouter(custom_base_name="basebone-app")

router.register("upload", upload_views.UploadViewSet)

urlpatterns = router.urls
