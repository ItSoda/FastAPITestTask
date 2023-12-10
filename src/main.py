from fastapi import FastAPI
from .app.router import router_order, router_trade_point, router_visit

app = FastAPI(
    title="FastAPITestTask"
)


app.include_router(router_trade_point)
app.include_router(router_order)
app.include_router(router_visit)