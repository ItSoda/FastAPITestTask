from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .app.router import (router_customer, router_order, router_trade_point,
                         router_visit, router_worker)

app = FastAPI(title="FastAPITestTask")

# Для подключения к реакту и флаттеру
origins = [
    "http://localhost:3000",
    "http://localhost:50000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT" "OPTIONS", "DELETE"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app.include_router(router_trade_point)
app.include_router(router_order)
app.include_router(router_visit)
app.include_router(router_worker)
app.include_router(router_customer)
