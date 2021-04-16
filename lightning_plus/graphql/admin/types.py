import graphene as gr


class TUser(gr.ObjectType):
    id = gr.Int()
    openid = gr.String()
    nickname = gr.String()
    sex = gr.String()
    avatar = gr.String()


class TActivity(gr.ObjectType):
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
    activity = gr.Field(TActivity)


class TFaceOrder(gr.ObjectType):
    id = gr.Int()
    image = gr.String()
    name = gr.String()
    user = gr.Field(TUser)
    template = gr.Field(TFaceTemplate)