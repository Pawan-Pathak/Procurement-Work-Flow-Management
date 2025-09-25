from __future__ import annotations
from datetime import datetime
from enum import Enum
from sqlalchemy import String, Integer, DateTime, Enum as SAEnum, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db


class RequestStatus(str, Enum):
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    UNDER_REVIEW = 'under_review'
    CLARIFICATION = 'clarification'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PO_GENERATED = 'po_generated'


class ProcurementRequest(db.Model):
    __tablename__ = 'requests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    justification: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[RequestStatus] = mapped_column(SAEnum(RequestStatus), default=RequestStatus.SUBMITTED, index=True)

    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    created_by = relationship('User')

    items = relationship('RequestItem', back_populates='request', cascade='all, delete-orphan')

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RequestItem(db.Model):
    __tablename__ = 'request_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey('requests.id'), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    request = relationship('ProcurementRequest', back_populates='items')

    def line_total(self) -> float:
        return float(self.quantity) * float(self.unit_price)