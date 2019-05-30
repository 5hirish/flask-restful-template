import os
import time
import pathlib

from datetime import datetime, date
from flask import Blueprint, Response, request, jsonify, session, send_file, current_app, g

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import and_, or_

from erpro.service.extensions import db
from erpro.worker.tasks import import_products
from erpro.service.product.models import ErpProductsModel

blue_print_name = 'product'
blue_print_prefix = '/product'

Model = db.Model

product_blueprint = Blueprint(blue_print_name, __name__, url_prefix=blue_print_prefix)


@product_blueprint.before_request
def perform_before_request():
    pass


@product_blueprint.route('/<string:file_type>/import', methods=["POST"])
def product_import(file_type):
    """
    Import CSV file of products and upsert the data.
    SKU is case insensitive.
    :param file_type: The type of import file
    :return: Job scheduled acknowledgement
    """

    allowed_file_extensions = set(['csv'])

    if file_type is not None and not request.stream.is_exhausted and file_type.lower() in allowed_file_extensions:
        static_file_path = current_app.config.get("STATIC_FILE_PATH")

        current_time_milli = str(round(time.time() * 1000))

        data_file_name = current_time_milli + "." + file_type.lower()
        data_file_path = os.path.join(static_file_path, data_file_name)

        total_streamed = 0

        if not os.path.exists(static_file_path):
            data_path = pathlib.Path(static_file_path)
            data_path.parent.mkdir(parents=True, exist_ok=True)
            if not os.path.exists(static_file_path):
                os.mkdir(static_file_path)

        with open(data_file_path, "bw") as data_file:
            chunk_size = 4096
            current_app.logger.debug("Stream Size:{0}".format(request.stream.limit))
            while not request.stream.is_exhausted:
                chunk = request.stream.read(chunk_size)
                total_streamed += chunk_size
                if len(chunk) == 0:
                    current_app.logger.debug("File saved at location:{0}".format(data_file_name))
                    break
                data_file.write(chunk)

        import_products.delay(data_file_path)

        return jsonify(
            {
                "status": "success",
                "msg": "Products scheduled for import",
            }
        ), 200

    return jsonify(
        {
            "status": "failure",
            "errorCode": "INVALID_PAYLOAD",
            "msg": "Products importing failed",
        }
    ), 200


@product_blueprint.route('/', methods=["GET"])
def product_search():
    """
    Search Products.
    Filter Products.
    :return: The matching products
    """

    product_sku = request.args.get("sku")
    product_name = request.args.get("name")
    product_status = request.args.get("status")

    if (product_sku is not None and product_sku != "") \
            or (product_name is not None and product_name != ""):
        product_results = []

        if product_sku is not None and product_sku != "":
            if product_status is not None and product_status != "":
                product_res = ErpProductsModel.query.filter_by(productSKU=product_sku, productStatus=product_status)\
                    .one_or_none()
            else:
                product_res = ErpProductsModel.query.filter_by(productSKU=product_sku).one_or_none()
            if product_res is not None:
                product_results = [product_res]

        elif product_name is not None and product_name != "":
            if product_status is not None and product_status != "":
                product_results = ErpProductsModel.query.filter(and_(
                    ErpProductsModel.productName.ilike('%' + product_name + '%'),
                    ErpProductsModel.productStatus == product_status
                )).all()

            else:
                product_results = ErpProductsModel.query.filter(
                    ErpProductsModel.productName.ilike('%' + product_name + '%')).all()
        else:
            product_results = None

        if product_results is not None and len(product_results) > 0:
            product_list = []
            for product in product_results:
                if product is not None:
                    product = {
                        "name": product.productName,
                        "sku": product.productSKU,
                        "description": product.productDescription,
                        "status": product.productStatus,
                        "modifiedOn": product.productModifiedOn
                    }
                    product_list.append(product)

            return jsonify({
                "status": "success",
                "msg": "Fetched {0} product".format(product_sku),
                "data": product_list
            }), 200

        else:
            return jsonify({
                "status": "failure",
                "msg": "No products found for the criteria",
                "errorCode": "NOT_FOUND"
            }), 200

    return jsonify(
        {
            "status": "failure",
            "msg": "Missing query parameters",
            "errorCode": "INVALID_PAYLOAD"
        }
    ), 200


@product_blueprint.route('/all', methods=["GET"])
def product_fetch():
    """
    View all of the products.
    Default page 1 and limit 100
    :return: Pagination
    """
    page_limit, page_num = 100, 1

    page_limit_str = request.args.get("limit", 100)
    page_num_str = request.args.get("page", 1)
    product_status = request.args.get("status")

    if page_limit_str is not None and page_limit_str != "":
        try:
            page_limit = int(page_limit_str)
        except ValueError:
            page_limit = 100

    if page_num_str is not None and page_num_str != "":
        try:
            page_num = int(page_num_str)
        except ValueError:
            page_num = 100

    if 0 < page_limit <= 1000 and 0 < page_num:

        total_products = ErpProductsModel.query.count()

        if product_status is not None and product_status != "":
            page_products = ErpProductsModel.query.filter_by(productStatus=product_status)\
                .paginate(page_num, per_page=page_limit, error_out=False)
        else:
            page_products = ErpProductsModel.query.paginate(page_num, per_page=page_limit, error_out=False)

        if page_products is not None and page_products.items is not None and len(page_products.items) > 0:
            list_products = []
            for cur_product in page_products.items:
                product = {
                    "name": cur_product.productName,
                    "description": cur_product.productDescription,
                    "status": cur_product.productStatus,
                    "modifiedOn": cur_product.productModifiedOn
                }

                list_products.append(product)

            return jsonify({
                "status": "success",
                "msg": "Fetched products {0}".format(len(list_products)),
                "totalProducts": total_products,
                "data": list_products
            }), 200

        return jsonify({
            "status": "failure",
            "msg": "Products fetch out of bounds",
            "errorCode": "NOT_FOUND"
        }), 200

    return jsonify(
        {
            "status": "failure",
            "msg": "Invalid page parameters",
            "errorCode": "INVALID_PAYLOAD"
        }
    ), 200


@product_blueprint.route('/', methods=["DELETE"])
def product_delete():
    """
    Delete all existing products
    :return:
    """

    db.session.query(ErpProductsModel).delete()
    db.session.commit()

    return jsonify(
        {
            "status": "success",
            "msg": "Deleted all products",
        }
    ), 200
