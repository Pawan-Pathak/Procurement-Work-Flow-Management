from datetime import datetime
from sqlalchemy import Integer, DateTime, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db


class Document(db.Model):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int | None] = mapped_column(ForeignKey('requests.id'), index=True, nullable=True)
    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(128), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(512), nullable=False)
    category: Mapped[str] = mapped_column(String(64), default='attachment')  # attachment|quote|po
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    request = relationship('ProcurementRequest')

    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)