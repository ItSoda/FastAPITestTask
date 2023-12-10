from fastapi import FastAPI

from .app.router import (
    router_customer,
    router_order,
    router_trade_point,
    router_visit,
    router_worker,
)

app = FastAPI(title="FastAPITestTask")


app.include_router(router_trade_point)
app.include_router(router_order)
app.include_router(router_visit)
app.include_router(router_worker)
app.include_router(router_customer)
