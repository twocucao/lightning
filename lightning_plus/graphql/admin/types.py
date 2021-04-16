import graphene as gr


class TActivity(gr.ObjectType):
    id = gr.Int()
    title = gr.String()
    image = gr.String()
    short_desc = gr.String()
    status = gr.String()
    type = gr.String()


class TSysGroup(gr.ObjectType):
    id = gr.Int()
    name = gr.String()


class TSysUser(gr.ObjectType):
    id = gr.Int()
    email = gr.String()
    date_joined = gr.DateTime()
    first_name = gr.String()
    username = gr.String()
    groups = gr.List(TSysGroup)
    is_active = gr.Boolean()
    is_staff = gr.Boolean()
    is_superuser = gr.Boolean()
    last_login = gr.DateTime()
    last_name = gr.String()
    permissions = gr.List(gr.String)
    user_permissions = gr.List(gr.String)


class TContentType(gr.ObjectType):
    id = gr.Int()
    app_label = gr.String()
    app_verbose_name = gr.String()
    model = gr.String()


class TSysPermission(gr.ObjectType):
    id = gr.Int()
    codename = gr.String()
    content_type = gr.String()
    display_name = gr.String()
    name = gr.String()


class TSetting(gr.ObjectType):
    logo = gr.String()
    title = gr.String()


class TMenu(gr.ObjectType):
    id = gr.Int()
    icon = gr.String()
    model = gr.String()
    name = gr.String()
    page = gr.String()
    parent_id = gr.Int()
    path = gr.String()
    sequence = gr.Int()
    # type: "group" , "item"
    type = gr.String()
    children = gr.List(lambda: TMenu)
