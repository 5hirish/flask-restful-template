from datetime import datetime

# from sqlalchemy.dialects.postgresql import VARCHAR, DATE, TEXT
from sqlalchemy.types import VARCHAR, DATE, TEXT  # Generic types

from foobar.service.extensions import sql_db

# Alias common SQLAlchemy names
Column = sql_db.Column
Relationship = sql_db.relationship
Model = sql_db.Model


class ErpProductsModel(Model):
    __tablename__ = 'products'

    product_sku = Column(VARCHAR(255), primary_key=True, nullable=False)
    product_name = Column(VARCHAR(255), nullable=False)
    product_description = Column(TEXT, nullable=True)
    product_status = Column(VARCHAR(15), default="inactive", nullable=False)
    product_modified_on = Column(DATE, default=datetime.utcnow, nullable=False)