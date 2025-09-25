from datetime import datetime
from enum import Enum
from sqlalchemy import Integer, DateTime, Enum as SAEnum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db


class ApprovalDecision(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    CLARIFY = 'clarify'


class Approval(db.Model):
    __tablename__ = 'approvals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey('requests.id'), index=True, nullable=False)
    approver_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    decision: Mapped[ApprovalDecision] = mapped_column(SAEnum(ApprovalDecision), default=ApprovalDecision.PENDING, index=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    request = relationship('ProcurementRequest')
    approver = relationship('User')

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)