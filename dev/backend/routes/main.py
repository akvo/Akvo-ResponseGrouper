from fastapi import APIRouter

main_route = APIRouter()


@main_route.get("/", tags=["Dev"])
def read_main():
    return "OK"
