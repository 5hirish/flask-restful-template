import csv
import io
from datetime import datetime
from celery.utils.log import get_task_logger

from erpro.service.extensions import db
from erpro.worker.core import celery_task, BaseTask
from erpro.service.product.models import ErpProductsModel

task_base_name = "erpro.worker."
logger = get_task_logger(__name__)


@celery_task.task(name=task_base_name + "import_products",
                  bind=False, max_retries=3, default_retry_delay=300, track_started=True,
                  base=BaseTask)
def import_products(chunk_str):

    chunk_str_io = io.StringIO(chunk_str)
    product_reader = csv.DictReader(chunk_str_io)
    for row in product_reader:
        if "name" and "sku" in row:
            erp_product = ErpProductsModel(
                productSKU=row.get("sku"),
                productName=row.get("name"),
                productDescription=row.get("description"),
                productModifiedOn=datetime.utcnow()
            )

            existing_product = ErpProductsModel.query.filter_by(productSKU=row.get("sku")).one_or_none()
            if existing_product is not None:
                db.session.merge(erp_product)
                db.session.flush()
            else:
                db.session.add(erp_product)

            logger.info("Committing data to database")

            db.session.commit()
