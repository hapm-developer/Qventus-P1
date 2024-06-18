from app.core.settings.app import AppSettings
from app.models.parts import Part as ModelPart
from fastapi.testclient import TestClient
from sqlalchemy import desc
from sqlalchemy.orm import Session


def test_create_part(client: TestClient, settings: AppSettings) -> None:
    response = client.post(
        f"{settings.api_v1_prefix}/parts/create/",
        json={
            "name": "Part A",
            "sku": "SKU001",
            "description": "Test Part",
            "weight_ounces": 15,
        },
    )
    assert response.status_code == 200


def test_read_part(client: TestClient, db_session: Session, settings: AppSettings) -> None:
    part_id = db_session.query(ModelPart).first().id
    response = client.get(f"{settings.api_v1_prefix}/parts/{part_id}")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data.keys()


def test_update_part(client: TestClient, db_session: Session, settings: AppSettings) -> None:
    part_id = db_session.query(ModelPart).first().id
    response = client.put(
        f"{settings.api_v1_prefix}/parts/update/{part_id}",
        json={
            "name": "Updated Part",
            "sku": "SKU001",
            "description": "Updated Description",
            "weight_ounces": 20,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Part"


def test_delete_part(client: TestClient, db_session: Session, settings: AppSettings) -> None:
    part_id = db_session.query(ModelPart).first().id
    response = client.delete(f"{settings.api_v1_prefix}/parts/delete/{part_id}")
    assert response.status_code == 200
    response = client.get(f"/{part_id}")
    assert response.status_code == 404


def test_read_nonexistent_part(
    client: TestClient, db_session: Session, settings: AppSettings
) -> None:
    max_id = db_session.query(ModelPart.id).order_by(desc(ModelPart.id)).first()
    nonexistent_id = max_id[0] + 100 if max_id else 1
    response = client.get(f"{settings.api_v1_prefix}/parts/{nonexistent_id}")
    assert response.status_code == 404


def test_update_nonexistent_part(
    client: TestClient, db_session: Session, settings: AppSettings
) -> None:
    max_id = db_session.query(ModelPart.id).order_by(desc(ModelPart.id)).first()
    nonexistent_id = max_id[0] + 100 if max_id else 1
    response = client.put(
        f"{settings.api_v1_prefix}/parts/update/{nonexistent_id}",
        json={
            "name": "Updated Part",
            "sku": "SKU001",
            "description": "Updated Description",
            "weight_ounces": 20,
        },
    )
    assert response.status_code == 404


def test_delete_nonexistent_part(
    client: TestClient, db_session: Session, settings: AppSettings
) -> None:
    max_id = db_session.query(ModelPart.id).order_by(desc(ModelPart.id)).first()
    nonexistent_id = max_id[0] + 100 if max_id else 1
    response = client.delete(f"{settings.api_v1_prefix}/parts/delete/{nonexistent_id}")
    assert response.status_code == 404
