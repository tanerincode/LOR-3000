from fastapi import APIRouter
from oven.compiler import compile_prompt
from oven.manager import PromptOven
from pydantic import BaseModel
from router_engine.router import choose_provider_and_respond

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    context_depth: int | None = 0
    format: str | None = "markdown"
    prompt_name: str | None = None
    prompt_vars: dict[str, str] | None = None


class ChatResponse(BaseModel):
    content: str
    provider: str


@router.post("", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    system_prompt: str | None = None
    if body.prompt_name:
        oven = PromptOven()
        record = oven.get(body.prompt_name)
        if record:
            system_prompt = compile_prompt(record, body.prompt_vars or {})

    content, provider = choose_provider_and_respond(
        prompt=body.message,
        context_depth=body.context_depth or 0,
        output_format=body.format or "markdown",
        system=system_prompt,
    )
    return ChatResponse(content=content, provider=provider)
