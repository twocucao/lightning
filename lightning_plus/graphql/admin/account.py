import graphene as gr

from lightning_plus.contrib.graphql.router import CreateForm, PartialForm, DeleteForm
from lightning_plus.graphql.admin.base import router


class TUser(gr.ObjectType):
    id = gr.Int()
    openid = gr.String()
    nickname = gr.String()
    sex = gr.String()
    avatar = gr.String()


class TFaceActivity(gr.ObjectType):
    id = gr.Int()
    title = gr.String()
    image = gr.String()
    short_desc = gr.String()
    status = gr.String()
    type = gr.String()


class TFaceTemplate(gr.ObjectType):
    id = gr.Int()
    name = gr.String()
    image = gr.String()
    activity = gr.Field(TFaceActivity)


class TFaceOrder(gr.ObjectType):
    id = gr.Int()
    image = gr.String()
    name = gr.String()
    user = gr.Field(TUser)
    template = gr.Field(TFaceTemplate)


@router.item("parallel", output=TFaceActivity)
def parallel():
    ...


@router.item("certification", output=TFaceActivity)
def certification():
    ...


class FormCreateFaceTemplate(CreateForm):
    activity_id = gr.Int(required=True)
    name = gr.String(required=True)
    image = gr.String(required=True)


@router.mutation
def create_face_template(form: FormCreateFaceTemplate):
    ...


class FormPartialFaceTemplate(PartialForm):
    id = gr.Int(required=True)
    name = gr.String(required=True)
    image = gr.String(required=True)


@router.mutation
def partial_face_template(form: FormPartialFaceTemplate):
    ...


class FormDeleteFaceTemplate(DeleteForm):
    id = gr.Int(required=True)


@router.mutation
def delete_face_template(form: FormDeleteFaceTemplate):
    ...
