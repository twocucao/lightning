from django.apps import AppConfig


class BsmConfigConfig(AppConfig):
    name = "bsm_config"
    verbose_name = "系统配置"

    def ready(self):
        from lightning_plus.bsm_config.bsm import functions
        from lightning_plus.bsm_config import signals
        from lightning_plus.api_basebone.restful.client.views import register_api

        register_api("auth", {"permission": {"actions": ["retrieve", "list", "set"]}})
