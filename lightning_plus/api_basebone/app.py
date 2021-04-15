from django.apps import AppConfig


class ApiBaseboneConfig(AppConfig):
    name = "lightning_plus.api_basebone"

    def ready(self):
        # import member.bsm.functions.form_id
        # from member import signals
        from lightning_plus.api_basebone.restful.client.views import register_api
        from lightning_plus.api_basebone.bsm.api import exposed
        import lightning_plus.api_basebone.bsm.functions  # 注册所有云函数
        from lightning_plus.api_basebone import db

        register_api(self.name, exposed)
