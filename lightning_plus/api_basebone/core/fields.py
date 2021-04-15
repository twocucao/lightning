import json
import typing
from django.db import models
from django.db.models import JSONField as OriginJSONField
from lightning_plus.api_basebone.core.object_model import ObjectModel
from lightning_plus.api_basebone.utils.timezone import local_timestamp


class BoneTimeStampField(models.BigIntegerField):
    description = "时间戳字段"

    def __init__(
        self, verbose_name=None, name=None, auto_now=False, auto_now_add=False, **kwargs
    ):
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        if self.auto_now or self.auto_now_add:
            kwargs["null"] = True
            kwargs["blank"] = True
        super().__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.auto_now:
            kwargs["auto_now"] = False
        if self.auto_now_add:
            kwargs["auto_now_add"] = False
        return name, path, args, kwargs

    def get_bsm_internal_type(self):
        return "BoneTimeStampField"

    def pre_save(self, model_instance, add):
        print(model_instance, self.attname, add, getattr(model_instance, self.attname))

        if self.auto_now or (self.auto_now_add and add):
            value = local_timestamp()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)


class BoneRichTextField(models.TextField):
    """富文本字段"""

    def get_bsm_internal_type(self):
        return "BoneRichTextField"


class BoneImageCharField(models.CharField):
    """存储图片的数据，以字符串的形式"""

    def get_bsm_internal_type(self):
        return "BoneImageCharField"


class BoneImageUrlField(models.CharField):
    """存储图片链接"""

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs.setdefault("max_length", 200)
        super().__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 200:
            del kwargs["max_length"]
        return name, path, args, kwargs

    def get_bsm_internal_type(self):
        return "BoneImageUrlField"


class BoneFileUrlField(models.URLField):
    """存储文件链接"""

    def get_bsm_internal_type(self):
        return "BoneFileUrlField"


class JSONField(OriginJSONField):
    ...


class ObjectField(JSONField):
    ...


class ArrayField(JSONField):
    def __init__(
        self,
        item_model: typing.Type[ObjectModel] = None,
        item_type: str = "string",
        **kwargs
    ):
        self.item_model = item_model or ObjectModel()
        self.item_type = "object" if item_model else item_type
        super(ArrayField, self).__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, [self.item_model], kwargs

    def get_bsm_internal_type(self):
        return "JsonArrayField"

    def from_db_value(self, value, expression, connection, context):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except:
                return []
        return value
