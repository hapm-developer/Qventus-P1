from collections import Counter
from typing import List

from app.models.parts import Part as ModelPart
from app.schemas.parts import Part, PartBase
from app.schemas.utils import WordCount
from sqlalchemy.orm import Session


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


def get_most_common_words(db: Session) -> List[WordCount]:
    # Fetch all parts from the database
    parts = db.query(ModelPart).all()

    print(parts)

    # Extract descriptions from parts and filter out None values
    descriptions = [part.description for part in parts if part.description]

    print(descriptions)

    # Split descriptions into words, convert to lowercase, and flatten the list
    words = []
    for description in descriptions:
        words.extend(description.lower().split())

    # Count occurrences of each word
    word_counts = Counter(words)

    # Get the 5 most common words
    most_common_words = word_counts.most_common(5)

    print(most_common_words)

    # Extract only the words (ignoring the counts) and return as a list
    return [WordCount(word=word, count=count) for word, count in most_common_words]
