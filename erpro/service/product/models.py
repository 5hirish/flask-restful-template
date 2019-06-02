from datetime import datetime

from sqlalchemy.dialects.postgresql import VARCHAR, DATE, TEXT
# from sqlalchemy.types import VARCHAR, DATE, TEXT  # Generic types

from erpro.service.extensions import db

# Alias common SQLAlchemy names
Column = db.Column
Relationship = db.relationship
Model = db.Model


class ErpProductsModel(Model):
    __tablename__ = 'erp_products'

    productSKU = Column(VARCHAR(255), primary_key=True, unique=True, nullable=False)
    productName = Column(VARCHAR(255), nullable=False)
    productDescription = Column(TEXT, nullable=True)
    productStatus = Column(VARCHAR(15), default="inactive", nullable=False)
    productModifiedOn = Column(DATE, default=datetime.utcnow, nullable=False)