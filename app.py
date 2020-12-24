from fastapi import FastAPI

from routers import standard_search, price_search


app = FastAPI()

app.include_router(standard_search.router)
app.include_router(price_search.router)
