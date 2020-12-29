from fastapi import FastAPI

from routers import cars, drom


tags_metadata = [
    {
        "name": "cars",
        "description": "Standard search process.",
    },
    {
        "name": "drom",
        "description": "drom.ru search process.",
    },
]

app = FastAPI(
    title="Spider API for CarsPass project",
    version="0.0.1",
    openapi_tags=tags_metadata,
)

app.include_router(cars.router)
app.include_router(drom.router)
