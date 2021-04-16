import typing
import inspect
from typing import List, Callable, Any, Dict

import graphene as gr
from graphene.utils.str_converters import to_camel_case
from pydantic import BaseModel


def smart_camel(s: str):
    return to_camel_case(s).capitalize()


def get_typed_signature(call: Callable) -> inspect.Signature:
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


def get_typed_annotation(param: inspect.Parameter, globalns: Dict[str, Any]) -> Any:
    annotation = param.annotation
    return annotation


def create_input_field(field_name, field_type, required=False) -> gr.InputField:
    if not required:
        return gr.InputField(field_type, out_name=field_name)
    else:
        return gr.InputField(gr.NonNull(field_type), out_name=field_name)


def transform_validator_field(field_name, field_schema, required=False):
    # validator
    if field_schema["type"] == "string":
        if field_schema.get("format", None) == "date":
            return create_input_field(field_name, gr.Date, required)
        if field_schema.get("format", None) == "date-time":
            return create_input_field(field_name, gr.DateTime, required)
        return create_input_field(field_name, gr.String, required)
    if field_schema["type"] == "integer":
        return create_input_field(field_name, gr.Int, required)
    raise NotImplementedError


def gen_args_from_validator(prefix, validator: BaseModel):
    schema = validator.schema()
    fields = {
        k: transform_validator_field(field_name=k, field_schema=v, required=True)
        for k, v in schema["properties"].items()
    }
    input_type_cls = type(
        f"{prefix}",
        (gr.InputObjectType,),
        fields,
    )
    return input_type_cls


class ResolverResult(typing.NamedTuple):
    resolver: typing.Callable
    parameters: typing.Mapping[str, inspect.Parameter]
    use_root: bool
    use_info: bool

    def get_item_kwargs(self):
        kwargs = {}
        use_id = self.parameters.get("id", False)
        if use_id:
            id_type = self.parameters["id"].annotation
            if id_type is inspect.Signature.empty:
                id_type = gr.Int
            # 转一下 inputtype
            kwargs["id"] = id_type(required=True)
        return kwargs

    def get_list_kwargs(self, name):
        name = smart_camel(name)
        kwargs = {}
        use_params = self.parameters.get("params", False)
        if use_params:
            params_type = self.parameters["params"].annotation
            args = gen_args_from_validator(f"P{name}", params_type)
            kwargs["params"] = args(required=True)
        return kwargs

    def get_pagination_kwargs(self, name):
        name = smart_camel(name)
        kwargs = {}
        use_params = self.parameters.get("params", False)
        if use_params:
            params_type = self.parameters["params"].annotation
            args = gen_args_from_validator(f"P{name}", params_type)
            kwargs["params"] = args(required=True)
        return kwargs

    def get_mutation_arguments_kwargs(self, name):
        name = smart_camel(name)
        kwargs = {}
        use_form = self.parameters.get("form", False)
        if use_form:
            form_type = self.parameters["form"].annotation
            args = gen_args_from_validator(f"V{name}", form_type)

            class Arguments:
                form = args(required=True)

            kwargs["Arguments"] = Arguments
        return kwargs


def parse_resolver(resolver_function):
    resolver_function_sig = get_typed_signature(resolver_function)

    use_root = resolver_function_sig.parameters.get("root", False)
    use_info = resolver_function_sig.parameters.get("info", False)

    def combine_resolver(root, info, *args, **kwargs):
        extra_kwargs = {}
        if use_info:
            extra_kwargs["info"] = info
        if use_root:
            extra_kwargs["root"] = root

        return resolver_function(*args, **kwargs, **extra_kwargs)

    return ResolverResult(
        resolver=combine_resolver,
        parameters=resolver_function_sig.parameters,
        use_root=use_root,
        use_info=use_info,
    )


class GqlRouter:
    query_fields: List
    mutation_fields: List
    namespace: str

    def __init__(self, namespace=None):
        self.namespace = namespace
        self.query_fields = []
        self.mutation_fields = []

    def item(self, name, output, *args, **kwargs):
        def decorate(resolver_function):
            resolver_result = parse_resolver(resolver_function)
            extra_kwargs = resolver_result.get_item_kwargs()
            field = gr.Field(
                output,
                *args,
                **kwargs,
                **extra_kwargs,
                resolver=resolver_result.resolver,
                description=resolver_function.__doc__ or "",
            )
            self.query_fields.append({"name": f"{name}", "field": field})
            return field

        return decorate

    def list(self, name, output, *args, **kwargs):
        def decorate(resolver_function):
            resolver_result = parse_resolver(resolver_function)
            extra_kwargs = resolver_result.get_list_kwargs(resolver_function.__name__)
            field = gr.Field(
                gr.List(output),
                *args,
                **extra_kwargs,
                **kwargs,
                resolver=resolver_result.resolver,
                description=resolver_function.__doc__ or "nops",
            )
            self.query_fields.append({"name": f"{name}", "field": field})
            return field

        return decorate

    def pagination(self, name: str, output, *args, **kwargs):
        def decorate(resolver_function):
            resolver_result = parse_resolver(resolver_function)
            extra_kwargs = resolver_result.get_pagination_kwargs(resolver_function.__name__)
            pagination_cls = type(
                f"TPagination{smart_camel(name)}",
                (gr.ObjectType,),
                {
                    "total": gr.Int(required=True),
                    "items": gr.NonNull(gr.List(gr.NonNull(output))),
                    "__init__": lambda *args, **kwargs: None
                },
            )
            field = gr.Field(
                pagination_cls,
                *args,
                **kwargs,
                **extra_kwargs,
                resolver=resolver_result.resolver,
                description=resolver_function.__doc__ or "nops",
            )
            self.query_fields.append({"name": f"{name}", "field": field})
            return field

        return decorate

    def mutation(self, name_or_fn, output=None, *args, **kwargs):
        def decorate(resolver_function, name):
            resolver_result = parse_resolver(resolver_function)

            field = type(
                resolver_function.__name__,
                (gr.Mutation,),
                dict(
                    **{
                        "Output": output or gr.Boolean,
                        "mutate": resolver_result.resolver,
                    },
                    **resolver_result.get_mutation_arguments_kwargs(resolver_function.__name__),
                ),
            ).Field(description=resolver_function.__doc__)
            self.mutation_fields.append({"name": name, "field": field})
            return field

        if callable(name_or_fn):
            return decorate(name_or_fn, name_or_fn.__name__)
        return lambda fn: decorate(fn, name_or_fn)

    def build_query_mixin(self, name: typing.Optional[str] = None) -> typing.Type:
        query_mixin = type(
            name or (self.namespace + "QueryMixin"),
            (gr.ObjectType,),
            {field["name"]: field["field"] for field in self.query_fields},
        )
        return query_mixin

    def build_mutation_mixin(self, name: typing.Optional[str] = None) -> typing.Type:
        mutation_mixin = type(
            name or (self.namespace + "MutationMixin"),
            (),
            {field["name"]: field["field"] for field in self.mutation_fields},
        )
        return mutation_mixin

    def inject_mutation(self, cls):
        for field in self.mutation_fields:
            setattr(cls, field["name"], field["field"])
        return cls

    def inject_query(self, cls):
        for field in self.query_fields:
            setattr(cls, field["name"], field["field"])
        return cls
