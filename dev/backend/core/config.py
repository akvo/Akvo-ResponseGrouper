from routes.main import main_route
from fastapi import FastAPI
from AkvoResponseGrouper.routes import collection_route

app = FastAPI(
    root_path="/api",
    title="Akvo Response Grouper Demo",
    version="1.0.0",
    contact={
        "name": "Akvo",
        "url": "https://akvo.org",
        "email": "tech.consultancy@akvo.org",
    },
    license_info={
        "name": "AGPL3",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
)

app.include_router(main_route)
app.include_router(collection_route)


@app.get("/", tags=["Dev"])
def read_main():
    return "OK"
