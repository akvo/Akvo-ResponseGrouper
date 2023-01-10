from fastapi import FastAPI
from fastapi.testclient import TestClient
from ..routes.collection import collection_route

app = FastAPI()
app.include_router(collection_route)
client = TestClient(app)


def test_get_index_collection():
    response = client.get(app.url_path_for("collection:get_index"))
    assert response.status_code == 200
    assert response.json() == [{"greeting": "Hello from collection"}]
