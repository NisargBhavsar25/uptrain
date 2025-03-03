"""This module hosts built-in checks for some common LLM evaluation tasks."""

from __future__ import annotations
import typing as t

from .checks import Check
from uptrain.operators import Histogram
from uptrain.operators import (
    ResponseFactualScore,
    ValidResponseScore,
    ResponseCompleteness,
    ResponseRelevance,
    ResponseConsistency,
    ResponseConciseness,
    ContextRelevance,
    PromptInjectionScore,
    LanguageCritique,
    ToneCritique,
    ResponseCompletenessWrtContext,
    GuidelineAdherenceScore,
    ResponseMatchingScore, 
    ConversationSatisfactionScore,
    CodeHallucinationScore,
    JailbreakDetectionScore,
)

# -----------------------------------------------------------
# Context related
# -----------------------------------------------------------

CheckContextRelevance = lambda: Check(
    name="score_context_relevance",
    operators=[ContextRelevance()],
    plots=[Histogram(x="score_context_relevance")],
)

CheckResponseFacts = lambda: Check(
    name="score_factual_accuracy",
    operators=[ResponseFactualScore()],
    plots=[Histogram(x="score_factual_accuracy")],
)

# -----------------------------------------------------------
# Response related
# -----------------------------------------------------------

CheckResponseCompleteness = lambda: Check(
    name="response_completeness_score",
    operators=[ResponseCompleteness()],
    plots=[Histogram(x="score_response_completeness")],
)

CheckResponseCompletenessWrtContext = lambda: Check(
    name="response_completeness_wrt_context_score",
    operators=[ResponseCompletenessWrtContext()],
    plots=[Histogram(x="score_response_completeness_wrt_context")],
)

CheckResponseRelevance = lambda: Check(
    name="response_relevance_score",
    operators=[ResponseRelevance()],
    plots=[Histogram(x="score_response_relevance")],
)

CheckResponseConsistency = lambda: Check(
    name="response_consistency_score",
    operators=[ResponseConsistency()],
    plots=[Histogram(x="score_response_consistency")],
)

CheckValidResponse = lambda: Check(
    name="valid_response_score",
    operators=[ValidResponseScore()],
    plots=[Histogram(x="score_valid_response")],
)

CheckResponseConciseness = lambda: Check(
    name="response_conciseness_score",
    operators=[ResponseConciseness()],
    plots=[Histogram(x="score_response_conciseness")],
)

CheckResponseMatching = lambda method = "llm": Check(
    name = f"{method}_score",
    operators=[ResponseMatchingScore(method=method)],
    plots=[Histogram(x=f"{method}_score")]
)

# -----------------------------------------------------------
# Language quality related
# -----------------------------------------------------------

CheckLanguageQuality = lambda: Check(
    name="language_critique_score",
    operators=[LanguageCritique()],
    plots=[
        Histogram(x="score_fluency"),
        Histogram(x="score_coherence"),
        Histogram(x="score_politeness"),
        Histogram(x="score_grammar"),
    ],
)

CheckToneQuality = lambda llm_persona: Check(
    name="tone_critique_score",
    operators=[ToneCritique(llm_persona=llm_persona)],
    plots=[Histogram(x="score_tone")],
)

# -----------------------------------------------------------
# Guideline related
# -----------------------------------------------------------

CheckGuidelineAdherence = lambda guideline, guideline_name="guideline", response_schema=None: Check(
    name = f"{guideline_name}_adherence_score",
    operators=[GuidelineAdherenceScore(guideline=guideline, guideline_name=guideline_name, response_schema=response_schema)],
    plots=[Histogram(x=f"score_{guideline_name}_adherence")]
)

# -----------------------------------------------------------
# Prompt Injection related
# -----------------------------------------------------------

CheckPromptInjection = lambda: Check(
    name = "prompt_injection_score",
    operators=[PromptInjectionScore()],
    plots=[Histogram(x="score_prompt_injection")]
)

# -----------------------------------------------------------
# Conversation related
# -----------------------------------------------------------

CheckConversationSatisfaction = lambda user_persona = "user", llm_persona = None : Check(
    name = "conversation_satisfaction_score",
    operators=[ConversationSatisfactionScore(user_persona, llm_persona)],
    plots=[Histogram(x=f"score_conversation_satisfaction")]
)

# -----------------------------------------------------------
# Code related
# -----------------------------------------------------------

CheckCodeHallucination = lambda: Check(
    name = "code_hallucination_score",
    operators=[CodeHallucinationScore()],
    plots=[Histogram(x="score_code_hallucination")]
)


# -----------------------------------------------------------
# Jailbreak related
# -----------------------------------------------------------

CheckJailbreakDetection = lambda: Check(
    name = "jailbreak_detection_score",
    operators=[JailbreakDetectionScore()],
    plots=[Histogram(x="score_jailbreak_attempted")]
)