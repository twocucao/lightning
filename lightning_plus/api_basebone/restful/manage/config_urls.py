"""
输出配置的路由
"""

from lightning_plus.api_basebone.drf.routers import BaseBoneSimpleRouter as SimpleRouter
from lightning_plus.api_basebone.restful.manage.config_views import ConfigViewSet

router = SimpleRouter(custom_base_name="schema-config")
router.register("", ConfigViewSet)

urlpatterns = router.urls
