import logging

from django.dispatch import receiver
from django.conf import settings
from django.db import models

from lightning_plus.api_basebone.core.fields import JSONField
from lightning_plus.api_basebone.signals import post_bsm_create, post_bsm_delete
from lightning_plus.api_basebone.settings import settings as basebone_settings

logger = logging.getLogger("django")


class AdminLog(models.Model):

    id = models.BigAutoField(primary_key=True)
    action_time = models.DateTimeField("发生时间", auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, verbose_name="用户"
    )

    action = models.CharField("动作", max_length=20, blank=True, default="")
    app_label = models.CharField("应用标识", max_length=20, blank=True, default="")
    model_slug = models.CharField("模型标识", max_length=30, blank=True, default="")
    object_id = models.CharField("数据ID", max_length=20, blank=True, default="")
    message = models.CharField("消息", max_length=50, blank=True, default="")
    params = JSONField(default=dict)

    class Meta:
        verbose_name = "动作日志记录"
        verbose_name_plural = "动作日志记录"


@receiver(post_bsm_create, dispatch_uid="__append_create_log")
def append_create_log(sender, instance, create, request, old_instance, scope, **kwargs):
    if (
        sender == AdminLog
        or not basebone_settings.MANAGE_USE_ACTION_LOG
        or scope != "admin"
    ):
        return
    try:
        action = "add" if create else "update"
        gmeta = getattr(sender, "GMeta", None)
        title_field = getattr(gmeta, "title_field", None) if gmeta else None

        AdminLog.objects.create(
            user=request.user,
            action=action,
            app_label=sender._meta.app_label,
            model_slug=sender._meta.model_name,
            object_id=instance.pk,
            params=request.data,
            message=getattr(instance, title_field) if title_field else repr(instance),
        )
    except:
        logger.error("append create log fail", exc_info=True)


@receiver(post_bsm_delete, dispatch_uid="__append_delete_log")
def append_delete_log(sender, instance, request, scope, **kwargs):
    print("增加删除的Log")
    if (
        sender == AdminLog
        or not basebone_settings.MANAGE_USE_ACTION_LOG
        or scope != "admin"
    ):
        return
    try:
        action = "delete"
        gmeta = getattr(sender, "GMeta", None)
        title_field = getattr(gmeta, "title_field", None) if gmeta else None

        AdminLog.objects.create(
            user=request.user,
            action=action,
            app_label=sender._meta.app_label,
            model_slug=sender._meta.model_name,
            object_id=instance.pk,
            message=getattr(instance, title_field) if title_field else repr(instance),
        )
    except:
        logger.error("append delete log fail", exc_info=True)
