import os
import time
import pathlib
import csv

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

        # import_products.delay(raw_text)
        with open(data_file_path, "r") as csv_file:
            product_reader = csv.DictReader(csv_file)
            for row in product_reader:
                if "name" and "sku" in row:
                    erp_product = ErpProductsModel(
                        productSKU=row.get("sku"),
                        productName=row.get("name"),
                        productDescription=row.get("description")
                    )

                    existing_product = ErpProductsModel.query.filter_by(productSKU=row.get("sku")).one_or_none()
                    if existing_product is not None:
                        existing_product = erp_product
                    else:
                        db.session.add(erp_product)

                    current_app.logger.info("Committing data to database")

                    db.session.commit()

        return jsonify(
            {
                "status": "success",
                "msg": "Products scheduled for import",
            }
        ), 200

    return jsonify(
        {
            "status": "failure",
            "msg": "Products scheduled for import",
        }
    ), 200


@product_blueprint.route('/', methods=["GET"])
def product_search():
    """
    View all of the products,
    Search Products.
    Filter Products.
    :return: The matching products
    """
    return jsonify(
        {
            "status": "success",
            "msg": "Fetched products",
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