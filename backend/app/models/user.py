from datetime import datetime
from enum import Enum
from sqlalchemy import String, Integer, DateTime, Enum as SAEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from ..extensions import db


class Role(str, Enum):
    REQUESTER = 'requester'
    COST_CENTER_HEAD = 'cost_center_head'
    ADMIN_TEAM = 'admin_team'
    FINANCE = 'finance'
    DFA = 'dfa'
    DOR = 'dor'
    PC = 'pc'
    ED = 'ed'
    PD = 'pd'
    SUPERADMIN = 'superadmin'


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[Role] = mapped_column(SAEnum(Role), nullable=False, index=True)

    # Auth fields (placeholder for integration)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def has_any_role(self, *roles: Role) -> bool:
        return self.role in roles

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User {self.email} ({self.role})>"