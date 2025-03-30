import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(320), unique=True, index=True, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False, nullable=False)

    files = relationship("File", back_populates="user", cascade="all, delete")


class File(Base):
    __tablename__ = 'file'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = Column(String(500), unique=True, nullable=False)
    filename = Column(String(255))

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id', ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    user = relationship("User", back_populates="files")
    is_deleted = Column(Boolean(), default=False)
