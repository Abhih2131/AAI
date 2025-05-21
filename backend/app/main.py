from fastapi import FastAPI
from app.core.database import database
from app.api.v1.endpoints.executive_summary import router as executive_summary_router

app = FastAPI(
    title="AAI HR BI Backend",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(executive_summary_router, prefix="/api/v1")
