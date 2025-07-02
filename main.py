from fastapi import FastAPI
from .import models
from .database import engine 
from.routers import product, seller, login

from typing import List


app=FastAPI(
    title="Product API",
    description="API for managing products and sellers",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "Support Team",
        "url": "https://example.com/support",
        "email": "demo@gmail.com"},
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    # docs_url="/documentation",
    # redoc_url=None # Disable ReDoc documentation
)
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

models.Base.metadata.create_all(engine)







