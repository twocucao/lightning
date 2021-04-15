from django.conf import settings
from lightning_plus.api_basebone.core.admin import register, BSMAdmin
from .. import models


@register
class RuleAdmin(BSMAdmin):
    # filter = ['model', 'groups']
    display = ["model", "groups"]
    form_fields = [
        "model"
        if hasattr(settings, "SHIELD_MODEL")
        else {"name": "model", "widget": "ModelSelect"},
        "groups",
        {
            "name": "condition",
            "params": {
                "canAdd": True,
                "fields": [
                    "field",
                    {"name": "operator", "disabled": "true"},
                    {"name": "variable", "disabled": "true"},
                ],
            },
        },
        {"name": "combinator", "widget": "Radio"},
    ]
    inline_actions = ["edit", "delete"]

    class Meta:
        model = models.Rule
