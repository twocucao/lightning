import graphene as gr

from lightning_plus.contrib.graphql.views import GraphQLView
from lightning_plus.graphql.admin.base import router


@router.inject_query
class QueryMixin:
    ...


class Query(QueryMixin, gr.ObjectType):
    can_query = gr.Boolean(default_value=True)


@router.inject_mutation
class MutationMixin:
    pass


class Mutation(MutationMixin, gr.ObjectType):
    can_mutation = gr.Boolean(default_value=True)
    ...


schema = gr.Schema(query=Query, mutation=Mutation)

graphql_view = GraphQLView.as_view(schema=schema)
