from typing import Optional

from lightning_plus.contrib.validator import Validator
from lightning_plus.graphql.admin.base import router
from lightning_plus.graphql.admin.types import TActivity


@router.item("activity", output=TActivity)
def activity():
    ...


@router.list("activity_list", output=TActivity)
def activity_list():
    ...


@router.pagination("activities", output=TActivity)
def activities():
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
