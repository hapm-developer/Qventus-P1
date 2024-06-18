from pydantic import BaseModel


class PartBase(BaseModel):
    name: str
    sku: str
    description: str | None = None
    weight_ounces: int
    is_active: bool = True


class Part(PartBase):
    id: int

    class Config:
        from_attributes = True
