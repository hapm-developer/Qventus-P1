from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.settings.app import AppSettings

def test_full_crud_flow(client: TestClient, settings: AppSettings):
    # Create
    response = client.post(
        f"{settings.api_v1_prefix}/parts/create/", 
        json={
            "name": "Part B", 
            "sku": "SKU002", 
            "description": "Test Part B", 
            "weight_ounces": 15,
        }
    )
    assert response.status_code == 200
    part_id = response.json()["id"]

    # Read
    response = client.get(f"{settings.api_v1_prefix}/parts/{part_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Part B"
    
    # List
    response = client.get(f"{settings.api_v1_prefix}/parts/list/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    # Update
    response = client.put(f"{settings.api_v1_prefix}/parts/update/{part_id}", json={"name": "Updated Part B", "sku": "SKU002", "description": "Updated Description", "weight_ounces": 25})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Part B"

    # Delete
    response = client.delete(f"{settings.api_v1_prefix}/parts/delete/{part_id}")
    assert response.status_code == 200

    # Verify Deletion
    response = client.get(f"{settings.api_v1_prefix}/parts/{part_id}")
    assert response.status_code == 404


def test_create_part_invalid_weight(client: TestClient, settings: AppSettings):
    response = client.post(
        f"{settings.api_v1_prefix}/parts/create/", 
        json={
            "name": "Invalid Part", 
            "sku": "INVALID001", 
            "description": "Invalid Part Description", 
            "weight_ounces": -5,
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Weight must be non-negative."
