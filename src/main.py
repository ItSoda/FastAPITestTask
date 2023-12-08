from fastapi import FastAPI
from .app.router import router as router_trade_point

app = FastAPI(
    title="FastAPITestTask"
)


app.include_router(router_trade_point)