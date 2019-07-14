from flask_restplus import fields

from foobar.service.schemas import SchemaCollection

product_search_payload_schema = {
        "sku": "Product SKU/Id",
        "name": "Name of the products",
        "limit": "Number products per page",
        "page": "Page number to iterate",
        "status": "Status of the products: ['active', 'inactive']",
}

product_status_payload_schema = {
        "status": "Status of the products: ['active', 'inactive']"
}


class ProductsCollectionSchema(SchemaCollection):

    def __init__(self, api_namespace):
        super().__init__(api_namespace)

    def define_schema(self, schema_name=None):

        self.schemas['product_schema'] = {
            "sku": fields.String(description="Product SKU/Id"),
            "name": fields.String(description="Name of the products"),
            "description": fields.String(description="Product description"),
            "status": fields.String(description="Status of the products", enum=['active', 'inactive']),
            "modifiedOn": fields.String(description="Account connected emails")
        }

        self.schemas['product_list_response_schema'] = {
            "data": fields.List(fields.Nested(self.get_marshaled_model('product_schema', 'Product Information'))),
            "totalProducts": fields.Integer(description="Total count of products fetched")
        }
