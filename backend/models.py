from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Job(Base):

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        String(36), primary_key=True
    )

    technician: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    notes: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30), default="pending", nullable=False
    )

    