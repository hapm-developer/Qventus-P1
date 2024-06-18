from typing import List

from app.api import deps, utils
from app.schemas.parts import Part, PartBase
from app.schemas.utils import WordCount
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/{part_id}",
    summary="Read a part by ID",
    response_description="Retrieve detailed information about a part by its ID",
    response_model=Part,
)
def read_part(part_id: int, db_session: Session = Depends(deps.get_db)) -> Part:
    """
    Retrieve a specific part by its ID.

    Args:
        part_id (int): The ID of the part to retrieve.
        db_session (Session, optional): SQLAlchemy database session.
        Defaults to Depends(deps.get_db).

    Returns:
        Part: Details of the retrieved part.

    Raises:
        HTTPException: If the part with the specified ID does not exist (404 Not Found).
    """
    db_part = utils.get_part(db=db_session, part_id=part_id)
    if not db_part:
        raise HTTPException(status_code=404, detail=f"Part with ID={part_id} not found.")
    return Part.model_validate(db_part)


@router.post(
    "/create/",
    summary="Create a new part",
    response_description="Create a new part object",
    response_model=Part,
)
def create_part(part: PartBase, db_session: Session = Depends(deps.get_db)) -> Part:
    """
    Create a new part.

    Args:
        part (PartCreate): Data required to create the new part.
        db_session (Session, optional): SQLAlchemy database session.
        Defaults to Depends(deps.get_db).

    Returns:
        Part: Newly created part details.

    Raises:
        HTTPException: If there is an issue creating the part,
        such as validation errors (400 Bad Request).
    """
    try:
        db_part = utils.create_part(db=db_session, part=part)
        return Part.model_validate(db_part)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.put(
    "/update/{part_id}",
    summary="Update an existing part",
    response_description="Update an existing part object",
    response_model=Part,
)
def update_part(part_id: int, part: PartBase, db_session: Session = Depends(deps.get_db)) -> Part:
    """
    Update an existing part by its ID.

    Args:
        part_id (int): The ID of the part to update.
        part (PartUpdate): Updated data for the part.
        db_session (Session, optional): SQLAlchemy database session.
        Defaults to Depends(deps.get_db).

    Returns:
        Part: Updated details of the part.

    Raises:
        HTTPException: If the part with the specified ID does not exist (404 Not Found).
    """
    db_part = utils.update_part(db=db_session, part_id=part_id, part=part)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return Part.model_validate(db_part)


@router.delete(
    "/delete/{part_id}",
    summary="Delete a part",
    description="Delete a part by its ID",
)
def delete_part(part_id: int, db_session: Session = Depends(deps.get_db)) -> None:
    """
    Delete a part by its ID.

    Args:
        part_id (int): The ID of the part to delete.
        db_session (Session, optional): SQLAlchemy database session.
        Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: If there is an issue deleting the part (500 Internal Server Error).
    """
    try:
        utils.delete_part(db=db_session, part_id=part_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Part not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete part: {str(e)}",
        )


@router.get(
    "/list/",
    summary="List parts",
    description="List all parts with optional pagination",
    response_model=List[Part],
)
def read_parts(
    skip: int = 0, limit: int = 10, db_session: Session = Depends(deps.get_db)
) -> List[Part]:
    """
    List parts with optional pagination.

    Args:
        skip (int, optional): Number of records to skip, Defaults to 0.
        limit (int, optional): Maximum number of records to retrieve, Defaults to 10.
        db_session (Session, optional): SQLAlchemy database session.
        Defaults to Depends(deps.get_db).

    Returns:
        List[Part]: List of parts within the specified range.

    """
    db_parts = utils.get_parts(db=db_session, skip=skip, limit=limit)
    return db_parts


@router.get(
    "/most_common_words/",
    summary="Get 5 most common words in part descriptions",
    response_description="List of the 5 most common words in part descriptions",
    response_model=List[WordCount],
)
def get_most_common_words(db_session: Session = Depends(deps.get_db)) -> List[WordCount]:
    """
    Endpoint to retrieve the 5 most common words in part descriptions.

    Returns:
    - List of the 5 most common words in part descriptions.
    """

    return utils.get_most_common_words(db=db_session)
