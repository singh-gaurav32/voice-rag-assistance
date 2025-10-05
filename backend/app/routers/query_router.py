from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.intent_service import IntentService, Intent
from app.services.rag_service import RAGService
from app.services.order_service import OrderService
from app.services.llm_factory import llm
from app.services.logger_service import LoggerService
import time

logger = LoggerService()

router = APIRouter(prefix="/query", tags=["Query"])


class QueryRequest(BaseModel):
    text: str = Field(..., min_length=3, description="User query text")


class QueryResponse(BaseModel):
    answer: str

intent_service = IntentService()
order_service = OrderService()
rag_service = RAGService.get_instance()

@router.post("/", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    start_time = time.time()
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    intent = intent_service.detect_intent(text)

    if intent == Intent.ORDER_STATUS:
        answer = order_service.handle_order_status(text)
    
    elif intent == Intent.RETURNS:
        top_chunks = await rag_service.retrieve_top_k_async(text, k=3)
        if not top_chunks:
            answer = "Sorry, I could not find an answer in the documents."
        else:
            answer = llm.generate_answer(text, top_chunks)
    else:  # FAQ or fallback
        answer = "Please ask about order status or returns."
    logger.log(f"Query: {text} \n Intent: {intent.name} \n Answer: {answer}")
    end_time = time.time()
    logger.log(f"\nProcessing time: {end_time - start_time:.2f} seconds")
    return QueryResponse(answer=answer)
