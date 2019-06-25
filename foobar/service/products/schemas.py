from flask_restplus import fields


product_search_payload_schema = {
    "sku": fields.String(description="Product SKU/Id"),
    "name": fields.String(description="Name of the products"),
    "limit": fields.Integer(description="Number products per page"),
    "page": fields.Integer(description="Page number to iterate"),
    "status": fields.String(description="Status of the products", enum=['active', 'inactive']),
}

product_schema = {
    "sku": fields.String(description="Product SKU/Id"),
    "name": fields.String(description="Name of the products"),
    "description": fields.String(description="Product description"),
    "status": fields.String(description="Status of the products", enum=['active', 'inactive']),
    "modifiedOn": fields.String(description="Account connected emails")
}

product_list_response_schema = {
    "data": fields.List(fields.Nested(product_schema)),
    "totalProducts": fields.Integer(description="Total count of products fetched")
}

