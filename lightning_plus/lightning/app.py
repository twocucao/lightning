import sys
from django.contrib.auth import get_user_model
from django.apps import AppConfig
from lightning_plus.api_basebone import module


class LightningConfig(AppConfig):
    name = "lightning_plus.lightning"

    def ready(self):
        user_model = get_user_model()
        path = user_model._meta.app_config.name + ".bsm." + module.BSM_FORM
        from .bsm import user_forms

        sys.modules[path] = user_forms
