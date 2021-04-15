from lightning_plus.api_basebone.utils.wechat.extension.logistics import WeChatLogistics
from lightning_plus.api_basebone.utils.wechat import wrap


def create_logistics(app_id):
    return wrap(WeChatLogistics, app_id)
