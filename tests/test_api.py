import pytest

test_data = {
    "name": "Leko",
    "image_url": "https://www.google.com/"
}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_analysis(client):
    response = client.post("/analyses", json=test_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Leko"
    assert response.json()["image_url"] == "https://www.google.com/"
    assert response.json()["status"] == "pending"
    assert response.json()["result"] is None
    assert "id" in response.json()
    assert "created_at" in response.json()


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "ab", "image_url": "https://example.com/a.png"},
        {"name": "x" * 101, "image_url": "https://example.com/a.png"},
        {"name": "Chest", "image_url": "not-a-url"},
        {"image_url": "https://example.com/a.png"},
    ],
    ids=["name_too_short", "name_too_long", "bad_url", "no_name"],
)
def test_create_analysis_invalid_payload(client, payload):
    assert client.post("/analyses", json=payload).status_code == 422


def test_list_analyses(client, created):
    response = client.get("/analyses")
    assert response.status_code == 200
    assert [a["id"] for a in response.json()] == [created["id"]]

def test_get_analysis(client, created):
    response = client.get(f"/analyses/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created

def test_get_analysis_not_found(client):
    assert client.get("/analyses/999").status_code == 404

def test_update_analysis_changes_only_passed_fields(client, created):
    response = client.patch(
        f"/analyses/{created['id']}",
        json={"status": "completed", "result": "no pathology"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["result"] == "no pathology"
    assert body["name"] == created["name"]

def test_update_analysis_invalid_status(client, created):
    response = client.patch(f"/analyses/{created['id']}", json={"status": "done"})
    assert response.status_code == 422

def test_update_analysis_not_found(client):
    response = client.patch("/analyses/999", json={"name": "new name"})
    assert response.status_code == 404  # сейчас упадёт: приложение отдаёт 500

def test_delete_analysis(client, created):
    assert client.delete(f"/analyses/{created['id']}").status_code == 200
    assert client.get(f"/analyses/{created['id']}").status_code == 404
    
def test_delete_analysis_not_found(client):
    assert client.delete("/analyses/999").status_code == 404  # сейчас упадёт: 500