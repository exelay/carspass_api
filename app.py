from fastapi import FastAPI

from routers import cars


tags_metadata = [
    {
        "name": "cars",
        "description": "Standard search process.",
    },
]

app = FastAPI(
    title="Spider API for CarsPass project",
    version="0.0.1",
    openapi_tags=tags_metadata,
)

app.include_router(cars.router)
