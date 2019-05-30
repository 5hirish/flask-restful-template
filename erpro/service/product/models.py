from erpro.service.extensions import db
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TIMESTAMP, DATE, TEXT, ARRAY, BOOLEAN, INTEGER
from sqlalchemy import ForeignKey, String, Integer, text
from datetime import datetime

# Alias common SQLAlchemy names
Column = db.Column
Relationship = db.relationship
Model = db.Model


class EmployeeLeaveModel(Model):
    __tablename__ = 'erp_products'

    pid = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    productName = Column(VARCHAR(255), nullable=False)
    productSKU = Column(VARCHAR(255), nullable=False)
    productDescription = Column(TEXT, nullable=False)
    productStatus = Column(VARCHAR(15), nullable=False)
    productModifiedOn = Column(DATE, nullable=True)