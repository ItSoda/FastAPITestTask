from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


trade_point = {"id": 1, "name": "itsoda"}


def test_worker_get():
    response = client.get("/worker/")
    assert response.status_code == 200


def test_worker_post():
    response = client.post(
        "/worker/create_worker", json={"id": 1, "name": "itsoda", "trade_point_id": 1}
    )
    assert response.status_code == 201
    assert response.json == {
        "status": 201,
        "data": {"id": 1, "name": "itsoda", "trade_point_id": 1},
        "detail": "Worker create successfully",
    }


def test_worker_patch():
    response = client.patch("/worker/partial_update_worker/{1}")
    assert response.status_code == 200


def test_worker_delete():
    response = client.delete("/worker/delete_worker/1")
    assert response.status_code == 200


# Пу пу пу....
