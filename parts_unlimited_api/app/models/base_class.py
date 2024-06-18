from typing import Any, Dict

from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def dict(cls) -> Dict[str, Any]:
        return cls.__dict__