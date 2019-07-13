from flask_restplus import fields


class SchemaCollection:

    cached_schemas = {}
    modelled_schemas = {}

    success_schema = {
        'status': fields.String(required=True),
        'msg': fields.String(required=True),
        # 'data': fields.Nested(),
    }

    error_schema = {
        'status': fields.String(required=True),
        'msg': fields.String(required=True),
        'errorCode': fields.String()
    }

    schemas = {
        'success_schema': success_schema,
        'error_schema': error_schema
    }

    def __init__(self, api_namespace):
        self.api_namespace = api_namespace

    def define_schema(self):
        pass

    def get_schema(self, schema_name):
        self.define_schema()
        return self.schemas.get(schema_name, None)

    def get_cached_schema(self, schema_name):
        if schema_name not in self.cached_schemas:
            self.cached_schemas[schema_name] = None
            self.cached_schemas[schema_name] = self.get_schema(schema_name)
        return self.cached_schemas[schema_name]

    def get_marshaled_model(self, schema_name, description='', inherit_from_schema=None):
        schema = self.get_cached_schema(schema_name)
        if schema is not None and schema_name not in self.modelled_schemas:
            if inherit_from_schema is None:
                model = self.api_namespace.model(description, schema)
                self.modelled_schemas[schema_name] = model
                return self.modelled_schemas[schema_name]
            else:
                inherited_model = self.get_marshaled_model(inherit_from_schema, description)
                model = self.api_namespace.inherit(description, inherited_model, schema)
                self.modelled_schemas[schema_name] = model
                return self.modelled_schemas[schema_name]
        elif schema_name in self.modelled_schemas:
            return self.modelled_schemas[schema_name]