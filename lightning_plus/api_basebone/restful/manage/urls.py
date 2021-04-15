from lightning_plus.api_basebone.drf.routers import BaseBoneSimpleRouter as SimpleRouter
from lightning_plus.api_basebone.restful.manage.views import CommonManageViewSet

router = SimpleRouter(custom_base_name="common-manage")
router.register("", CommonManageViewSet)

urlpatterns = router.urls
