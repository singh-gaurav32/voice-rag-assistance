from pydantic import ValidationError


def validate_text_input(text: str):
    if not text or len(text.strip()) < 3:
        raise ValidationError("Text input too short.")