from fastapi import FastAPI

from routers import standard_search


tags_metadata = [
    {
        "name": "standard_search",
        "description": "Standard search process.",
    },
]

app = FastAPI(
    title="Spider API for CarsPass project",
    version="0.0.1",
    openapi_tags=tags_metadata,
)

app.include_router(standard_search.router)
