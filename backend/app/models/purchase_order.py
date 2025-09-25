from datetime import datetime
from sqlalchemy import Integer, DateTime, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db


class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey('requests.id'), nullable=False, index=True)
    po_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    vendor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items = relationship('PurchaseOrderItem', back_populates='purchase_order', cascade='all, delete-orphan')


class PurchaseOrderItem(db.Model):
    __tablename__ = 'purchase_order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purchase_order_id: Mapped[int] = mapped_column(ForeignKey('purchase_orders.id'), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    purchase_order = relationship('PurchaseOrder', back_populates='items')