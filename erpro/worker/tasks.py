import csv
import codecs
import io
from datetime import datetime
from celery.utils.log import get_task_logger

from erpro.service.extensions import db
from erpro.worker.core import celery_task, BaseTask
from erpro.service.product.models import ErpProductsModel
from erpro.utils import get_aws_client

task_base_name = "erpro.worker."
logger = get_task_logger(__name__)


@celery_task.task(name=task_base_name + "import_products",
                  bind=False, max_retries=3, default_retry_delay=300, track_started=True,
                  base=BaseTask)
def import_products(file_name):
    """
    Celery task to stream file from bucket and iterate over to upsert data into database.
    :param file_name: S3 file name or Key
    :return: None
    """

    file_stream = None

    s3_client = get_aws_client('s3',
                               celery_task.conf.get("AWS_ACCESS_KEY"),
                               celery_task.conf.get("AWS_SECRET_ACCESS_KEY"))

    s3_bucket_name = celery_task.conf.get("AWS_S3_PRODUCT_BUCKET")

    try:
        file_object_resp = s3_client.get_object(Bucket=s3_bucket_name, Key=file_name)
        if file_object_resp is not None and file_object_resp.get("ContentLength") is not None:
            file_stream = codecs.getreader('utf-8')(file_object_resp.get("Body"))

    except Exception as e:
        # botocore.errorfactory.NoSuchKey
        logger.exception(e)

    if file_stream is not None:
        product_reader = csv.DictReader(file_stream)

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

        response = s3_client.delete_object(Bucket=s3_bucket_name, Key=file_name)
        logger.info("File deleted from bucket: {0}".format(response))