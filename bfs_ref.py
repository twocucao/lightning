schema = {
    'title': 'VLogin',
    'type': 'object',
    'properties': {
        'name': {
            'title': 'Name',
            'default': '123',
            'type': 'string',
        },
        'date': {
            'title': 'Date',
            'type': 'string',
            'format': 'date',
        },
        'datetime': {
            'title': 'Datetime',
            'type': 'string',
            'format': 'date-time',
        },
        'password': {
            'title': 'Password',
            'type': 'string',
        },
        'type': {
            '$ref': '#/definitions/EnumLoginType',
        },
        'types': {
            'type': 'array',
            'items': {
                '$ref': '#/definitions/EnumLoginType',
            },
        },
        'items': {
            'title': 'Items',
            'type': 'array',
            'items': {
                '$ref': '#/definitions/Item',
            },
        },
    },
    'required': [
        'date',
        'datetime',
        'type',
        'types',
        'items',
    ],
    'definitions': {
        'EnumLoginType': {
            'title': 'EnumLoginType',
            'description': 'An enumeration.',
            'enum': [
                'CODE',
                'PASSWORD',
            ],
            'type': 'string',
        },
        'NestItem': {
            'title': 'NestItem',
            'type': 'object',
            'properties': {
                'type': {
                    '$ref': '#/definitions/EnumLoginType',
                },
                'id': {
                    'title': 'Id',
                    'type': 'integer',
                },
            },
            'required': [
                'type',
                'id',
            ],
        },
        'Item': {
            'title': 'Item',
            'type': 'object',
            'properties': {
                'id': {
                    'title': 'Id',
                    'type': 'integer',
                },
                'name': {
                    'title': 'Name',
                    'type': 'string',
                },
                'nest_item': {
                    'title': 'Nest Item',
                    'type': 'array',
                    'items': {
                        '$ref': '#/definitions/NestItem',
                    },
                },
            },
            'required': [
                'id',
                'name',
                'nest_item',
            ],
        },
    },
}

visited = []


def resolve_pydantic_schema(visited, schema):
    if definitions := schema.get("definitions", {}):
        for def_type, def_schema in definitions.items():
            ...

    if node not in visited:

        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)


dfs(visited, schema)


def bfs_ref(visited, graph, node):
    visited.append(node)
    queue.append(node)
    for field_type, field_schema in schema["definitions"].items():
        definitions[f"#/definitions/{field_type}"] = field_schema
        if field_schema["type"] == 'object':
            for def_field_name, def_field_schema in field_schema["properties"].items():
                ...
            resolve_properties()
            ...
        ...
    for key, value in schema["properties"].items():
        if ref := value.get("$ref", None):
            tobe_resolved_definition[key] = value

    while queue:
        s = queue.pop(0)
        print(s, end=" ")

        for neighbour in graph[s]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)


# Driver Code
bfs_ref(visited, schema)
