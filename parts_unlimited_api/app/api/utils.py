from typing import List
from sqlalchemy.orm import Session

from app.models.parts import Part as ModelPart
from app.schemas.parts import Part, PartBase


def create_part(db: Session, part: PartBase) -> ModelPart:
    db_part = ModelPart(**part.model_dump())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

def get_part(db: Session, part_id: int) -> ModelPart:
    return db.query(ModelPart).filter(ModelPart.id == part_id).first()

def get_parts(db: Session, skip: int = 0, limit: int = 10) -> List[Part]:
    return db.query(ModelPart).offset(skip).limit(limit).all()

def update_part(db: Session, part_id: int, part: PartBase) -> ModelPart:
    db_part = db.query(ModelPart).filter(ModelPart.id == part_id).first()
    if db_part:
        for attr, value in vars(part).items():
            setattr(db_part, attr, value) if value is not None else None
        db.commit()
        db.refresh(db_part)
    return db_part

def delete_part(db: Session, part_id: int) -> None:
    db_part = db.query(ModelPart).filter(ModelPart.id == part_id).first()
    if db_part:
        db.delete(db_part)
        db.commit()
    else:
        raise ValueError(f"ID: {part_id} not found, please try with a valid ID")