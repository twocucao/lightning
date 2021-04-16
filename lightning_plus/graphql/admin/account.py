import datetime
import enum
from typing import Optional

from lightning_plus.contrib.validator import Validator
from lightning_plus.graphql.admin.base import router
from lightning_plus.graphql.admin.types import TActivity, TSysUser, TSetting, TSysGroup


@router.item("activity", output=TActivity)
def activity():
    ...


@router.item("profile", output=TSysUser)
def profile():
    ...


@router.item("settings", output=TSetting)
def settings():
    ...


@router.pagination("sys_users", output=TSysUser)
def sys_users():
    ...


@router.pagination("sys_groups", output=TSysGroup)
def sys_groups():
    ...


@router.item("admin_schema", output=TSysGroup)
def admin_schema():
    ...


@router.list("activity_list", output=TActivity)
def activity_list():
    return [
        {
            "id": 2
        }
    ]


@router.pagination("activities", output=TActivity)
def activities():
    return [
        {
            "id": 2
        }
    ]


class EnumLoginType(str, enum.Enum):
    CODE = "CODE"
    PASSWORD = "PASSWORD"


class VLogin(Validator):
    name: str = "123"
    date: datetime.date
    datetime: datetime.datetime
    password: Optional[str]
    # type: EnumLoginType
    # types: list[EnumLoginType]

    # class Item(Validator):
    #     id: int
    #     name: str
    #
    #     class NestItem(Validator):
    #         type: EnumLoginType
    #         id: int
    #
    #     nest_item: list[NestItem]
    #
    # items: list[Item]


@router.mutation("login", output=TSysUser)
def login(form: VLogin):
    ...


class VCreate(Validator):
    activity_id: int
    name: str
    image: str


@router.mutation
def create_face_template(form: VCreate):
    ...


class VPartial(Validator):
    activity_id: int
    name: Optional[str]
    image: str = "123"


@router.mutation
def partial_face_template(form: VPartial):
    ...


class VDelete(Validator):
    id: int


@router.mutation
def delete_face_template(form: VDelete):
    ...
