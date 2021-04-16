from graphene.types.generic import GenericScalar
from graphene.utils.str_converters import to_camel_case, to_snake_case


class AutoJSON(GenericScalar):
    @classmethod
    def serialize(cls, value):
        value = super().serialize(value)
        return convert_keys(value, to_camel_case)

    @classmethod
    def parse_literal(cls, node):
        value = super().parse_literal(node)
        return convert_keys(value, to_snake_case)

    @classmethod
    def parse_value(cls, value):
        value = super().parse_value(value)
        return convert_keys(value, to_snake_case)


def convert_keys(data, to):
    """
    Convert object keys either to camelCase or to snake_case
    @param data: object - processed recursively
    @param to: callable - applied to each key of each object found
    """
    if isinstance(data, dict):
        return {to(key): convert_keys(value, to) for key, value in data.items()}

    if isinstance(data, (list, tuple)):
        return [convert_keys(value, to) for value in data]

    return data
