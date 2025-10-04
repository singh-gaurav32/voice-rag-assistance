from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import query_router


app = FastAPI(title="Voice RAG Customer-Care Assistant")


# Allow browser client for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(query_router.router)


@app.get("/")
def root():
    return {"message": "Voice RAG Assistant API is running!"}