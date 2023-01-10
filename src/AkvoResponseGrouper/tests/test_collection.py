from fastapi import FastAPI
from fastapi.testclient import TestClient
from ..routes import collection

app = FastAPI()
app.include_router(collection.router)
client = TestClient(app)


def test_get_index_collection():
    response = client.get("/collection")
    assert response.status_code == 200
    assert response.json() == [{"greeting": "Hello from collection"}]
