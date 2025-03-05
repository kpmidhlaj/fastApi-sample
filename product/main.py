from fastapi import FastAPI

from . import models
from .database import engine

from .routers import product, seller, login

app = FastAPI(
    title="Products API",
    description="API for managing products",
    # terms_of_service="http://example.com/terms/",
    # contact={
    #     "name": "John Doe",
    #     "url": "http://x-force.com/contact",
    #     "email": "WtG3P@example.com"
    # },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0"
    # },
    # docs_url="/documentation",
    redoc_url=None
)
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)
models.Base.metadata.create_all(bind=engine)
