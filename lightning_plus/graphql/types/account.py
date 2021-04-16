import graphene as gr

from lightning_plus.contrib.graphql.fields import AutoJSON


class TUserLogin(gr.ObjectType):
    id = gr.Int()
    token = gr.String()


class TKidRound(gr.ObjectType):
    next_round = gr.Field(lambda: TKidRound)

    id = gr.Int()
    lesson_id = gr.Int()
    name = gr.String()
    type = gr.String()
    order_num = gr.Int()
    stars = gr.String()
    cover = gr.String()
    audio = gr.String()
    detail = AutoJSON()


class TKidLesson(gr.ObjectType):
    id = gr.Int()
    no = gr.Int()
    name = gr.String()
    type = gr.String()
    status = gr.String()
    days = gr.Int()
    thumbnail = gr.String()
    words_count = gr.Int()


class TKidTopic(gr.ObjectType):
    id = gr.Int()
    name = gr.String()
    title = gr.String()
    desc = gr.String()
    order_num = gr.Int()

    lessons = gr.List(TKidLesson)


class TKidCourse(gr.ObjectType):
    id = gr.Int()
    name = gr.String()
    order_num = gr.Int()
    status = gr.String()
    thumbnail = gr.String()

    topics = gr.List(TKidTopic)
