from fastapi import APIRouter, Request
from twilio.twiml.voice_response import VoiceResponse
from app.services.intent_service import IntentService
from app.services.order_service import OrderService
from app.services.rag_service import RAGService
from app.utils.utility import generate_tts_response
from starlette.responses import Response

router = APIRouter(prefix="/twilio", tags=["Twilio"])

intent_service = IntentService()
order_service = OrderService()
rag_service = RAGService.get_instance()


@router.post("/voice")
async def handle_voice(request: Request):
    # Parse Twilio's request
    form_data = await request.form()
    user_input = form_data.get("SpeechResult", "").strip()

    if not user_input:
        response = VoiceResponse()
        response.say("Sorry, I didn't catch that. Please try again.")
        return Response(content=str(response), media_type="application/xml")

    # Detect intent and generate a response
    intent = intent_service.detect_intent(user_input)
    if intent == "order_status":
        answer = order_service.handle_order_status(user_input)
    else:
        answer = rag_service.handle_faq_query(user_input)

    # Generate TTS audio file
    audio_file = generate_tts_response(answer)

    # Respond with Twilio's Play verb
    response = VoiceResponse()
    #TODO Decide when to delete the file later
    response.play(audio_file)  # Twilio will play the audio file
    return Response(content=str(response), media_type="application/xml")