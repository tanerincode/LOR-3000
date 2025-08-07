from fastapi import APIRouter
from pydantic import BaseModel
from router_engine.router import choose_provider_and_respond

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    context_depth: int | None = 0
    format: str | None = "markdown"


class ChatResponse(BaseModel):
    content: str
    provider: str


@router.post("", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    content, provider = choose_provider_and_respond(
        prompt=body.message,
        context_depth=body.context_depth or 0,
        output_format=body.format or "markdown",
    )
    return ChatResponse(content=content, provider=provider)
