import pytest
from fastapi import status


def sample_product_payload(
    name="Industrial Electric Motor",
    category="finished",
    description="High-torque 3-phase AC induction motor",
    product_image="https://example.com/images/motor.jpg",
    sku="MOT-IND-001",
    unit_of_measure="unit",
    lead_time=14
):
    return {
        "name": name,
        "category": category,
        "description": description,
        "product_image": product_image,
        "sku": sku,
        "unit_of_measure": unit_of_measure,
        "lead_time": lead_time
    }


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "online"
    assert "endpoints" in data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_create_product_success(client):
    payload = sample_product_payload()
    response = client.post("/product/add", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == payload["name"]
    assert data["category"] == payload["category"]
    assert data["description"] == payload["description"]
    assert data["product_image"] == payload["product_image"]
    assert data["sku"] == payload["sku"]
    assert data["unit_of_measure"] == payload["unit_of_measure"]
    assert data["lead_time"] == payload["lead_time"]
    assert "created_date" in data
    assert "updated_date" in data


@pytest.mark.parametrize("category", ["finished", "semi-finished", "raw"])
def test_create_product_all_categories(client, category):
    payload = sample_product_payload(category=category, sku=f"SKU-{category}")
    response = client.post("/product/add", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["category"] == category


@pytest.mark.parametrize("uom", ["mtr", "mm", "ltr", "ml", "cm", "mg", "gm", "unit", "pack"])
def test_create_product_all_uoms(client, uom):
    payload = sample_product_payload(unit_of_measure=uom, sku=f"SKU-{uom}")
    response = client.post("/product/add", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["unit_of_measure"] == uom


def test_create_product_invalid_category(client):
    payload = sample_product_payload(category="invalid-category")
    response = client.post("/product/add", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_product_invalid_uom(client):
    payload = sample_product_payload(unit_of_measure="kg")  # 'kg' is not in spec ('gm', 'mg' are)
    response = client.post("/product/add", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_product_negative_lead_time(client):
    payload = sample_product_payload(lead_time=-5)
    response = client.post("/product/add", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_product_empty_name(client):
    payload = sample_product_payload(name="")
    response = client.post("/product/add", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_product_description_too_long(client):
    payload = sample_product_payload(description="a" * 251)
    response = client.post("/product/add", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_product_info_success(client):
    payload = sample_product_payload()
    created = client.post("/product/add", json=payload).json()
    pid = created["id"]

    response = client.get(f"/product/{pid}/info")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == pid
    assert data["name"] == payload["name"]


def test_get_product_info_not_found(client):
    response = client.get("/product/99999/info")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_update_product_success(client):
    payload = sample_product_payload()
    created = client.post("/product/add", json=payload).json()
    pid = created["id"]

    update_payload = {
        "name": "Updated Motor v2",
        "category": "semi-finished",
        "lead_time": 21
    }
    response = client.put(f"/product/{pid}/update", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == pid
    assert data["name"] == "Updated Motor v2"
    assert data["category"] == "semi-finished"
    assert data["lead_time"] == 21
    assert data["sku"] == payload["sku"]  # Unchanged field remains intact


def test_update_product_not_found(client):
    response = client.put("/product/99999/update", json={"name": "Ghost Product"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_product_invalid_data(client):
    payload = sample_product_payload()
    created = client.post("/product/add", json=payload).json()
    pid = created["id"]

    response = client.put(f"/product/{pid}/update", json={"lead_time": -10})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_list_products_empty(client):
    response = client.get("/product/list")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["items"] == []
    assert data["total_records"] == 0
    assert data["current_page"] == 1
    assert data["page_size"] == 10
    assert data["total_pages"] == 1
    assert data["has_next"] is False
    assert data["has_previous"] is False


def test_list_products_pagination_10_per_page(client):
    # Insert 25 products
    for i in range(1, 26):
        payload = sample_product_payload(
            name=f"Product {i:02d}",
            sku=f"SKU-{i:03d}",
            lead_time=i
        )
        client.post("/product/add", json=payload)

    # Fetch page 1 (default limit = 10)
    page1 = client.get("/product/list?page=1").json()
    assert page1["total_records"] == 25
    assert page1["current_page"] == 1
    assert page1["page_size"] == 10
    assert page1["total_pages"] == 3
    assert len(page1["items"]) == 10
    assert page1["has_next"] is True
    assert page1["has_previous"] is False
    assert page1["items"][0]["name"] == "Product 01"
    assert page1["items"][9]["name"] == "Product 10"

    # Fetch page 2
    page2 = client.get("/product/list?page=2").json()
    assert page2["current_page"] == 2
    assert len(page2["items"]) == 10
    assert page2["has_next"] is True
    assert page2["has_previous"] is True
    assert page2["items"][0]["name"] == "Product 11"

    # Fetch page 3
    page3 = client.get("/product/list?page=3").json()
    assert page3["current_page"] == 3
    assert len(page3["items"]) == 5
    assert page3["has_next"] is False
    assert page3["has_previous"] is True
    assert page3["items"][4]["name"] == "Product 25"
