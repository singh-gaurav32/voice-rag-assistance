from fastapi import APIRouter
from app.routers import query_router


api_router = APIRouter()
api_router.include_router(query_router.router)