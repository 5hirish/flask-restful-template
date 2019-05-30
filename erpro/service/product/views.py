import os
from datetime import datetime, date
from flask import Blueprint, Response, request, jsonify, session, send_file, current_app, g

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import and_, or_

from erpro.service.extensions import db

blue_print_name = 'product'
blue_print_prefix = '/product'

Model = db.Model

product_blueprint = Blueprint(blue_print_name, __name__, url_prefix=blue_print_prefix)


@product_blueprint.before_request
def perform_before_request():
    pass


@product_blueprint.route('/{file_type:string}/import', methods=["POST"])
def product_import(file_type):
    """
    Import CSV file of products and upsert the data.
    SKU is case insensitive.
    :param file_type: The type of import file
    :return: Job scheduled acknowledgement
    """
    return jsonify(
        {
            "status": "success",
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
    return jsonify(
        {
            "status": "success",
            "msg": "Deleted all products",
        }
    ), 200