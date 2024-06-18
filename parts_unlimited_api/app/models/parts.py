from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from app.models.base_class import Base

class Part(Base):

    name = Column(String(150), nullable=False)
    sku = Column(String(30), unique=True, index=True)
    description = Column(String(1024))
    weight_ounces = Column(Integer)
    
    @validates('weight_ounces')
    def validate_weight_ounces(self, key: str, value: int) -> int:
        if value < 0:
            raise ValueError("Weight must be non-negative.")
        return value