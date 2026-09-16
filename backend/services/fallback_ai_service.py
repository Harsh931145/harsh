from typing import List, Optional, Tuple


class FallbackAIService:
    """Try multiple AI providers in order, falling back on provider failures."""

    def __init__(self, providers: List[Tuple[str, object]]):
        self.providers = providers

    async def answer_question(
        self,
        question: str,
        image_base64: Optional[str] = None,
    ) -> Tuple[str, List[str], float]:
        last_answer = "AI service unavailable. Please try again.", [], 0.0

        for provider_name, provider in self.providers:
            answer, sources, confidence = await provider.answer_question(
                question=question,
                image_base64=image_base64,
            )

            if _should_stop_without_fallback(answer):
                return answer, sources, confidence

            if not _is_provider_failure(answer, confidence):
                if provider_name.lower() != "groq":
                    print(f"Answered using fallback provider: {provider_name}")
                return answer, sources, confidence

            print(f"{provider_name} unavailable, trying next provider: {answer}")
            last_answer = answer, sources, confidence

        return last_answer


def _should_stop_without_fallback(answer: str) -> bool:
    answer_lower = (answer or "").lower()
    return "knowledge base" in answer_lower and (
        "couldn't find relevant" in answer_lower
        or "upload exam materials" in answer_lower
    )


def _is_provider_failure(answer: str, confidence: float) -> bool:
    answer_lower = (answer or "").lower()
    failure_markers = (
        "rate limit",
        "too many requests",
        "ai service not configured",
        "api key",
        "error generating answer",
        "error calling",
        "answer unavailable",
        "please wait",
        "try again",
    )
    return confidence <= 0 and any(marker in answer_lower for marker in failure_markers)
