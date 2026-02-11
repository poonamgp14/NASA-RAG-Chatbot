from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from typing import Dict, List, Optional
import os
from datasets import Dataset
import asyncio

# RAGAS imports
try:
    from ragas import SingleTurnSample
    from ragas.metrics.collections import BleuScore, RougeScore
    from ragas.metrics import NonLLMContextPrecisionWithReference, ResponseRelevancy, Faithfulness
    from ragas import evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False



async def evaluate_response_quality(question: str, answer: str, contexts: List[str]) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics"""
    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}
    
    # TODO: Create evaluator LLM with model gpt-3.5-turbo
    # TODO: Create evaluator_embeddings with model test-embedding-3-small
    # TODO: Define an instance for each metric to evaluate
    # TODO: Evaluate the response using the metrics
    # TODO: Return the evaluation results
    open_ai_api = os.getenv("OPENAI_API_KEY")
    open_ai_url = "https://api.openai.com/v1"

    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key= open_ai_api,
            base_url= open_ai_url,
            temperature=0.0
    ))
    evaluator_embeddings = LangchainEmbeddingsWrapper(
            OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=open_ai_api
            )
        )
    results = {}
    # Convert to RAGAS-compatible format
    scorer = BleuScore()
    # Evaluate
    resultBleuScore = scorer.ascore(
        reference="The Eiffel Tower is located in Paris.",
        response="The Eiffel Tower is located in India."
    )
    results['BleuScore'] = resultBleuScore.value
    
    # Create metric (no LLM/embeddings needed)
    scorerRouge = RougeScore(rouge_type="rougeL", mode="fmeasure")

# Evaluate
    resultRougeScore = await scorerRouge.ascore(
        reference="The Eiffel Tower is located in Paris.",
        response="The Eiffel Tower is located in India."
    )
    results['RougeScore'] = resultRougeScore.value

    context_precision = NonLLMContextPrecisionWithReference()

    sample = SingleTurnSample(
        retrieved_contexts=["The Eiffel Tower is located in Paris."],
        reference_contexts=["Paris is the capital of France.", "The Eiffel Tower is one of the most famous landmarks in Paris."]
    )

    results['NonLLMContextPrecisionWithReference'] = await context_precision.single_turn_ascore(sample)

    sampleResponseRelevancy = SingleTurnSample(
        user_input="When was the first super bowl?",
        response="The first superbowl was held on Jan 15, 1967",
        retrieved_contexts=[
            "The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles."
        ]
    )

    scorerResponseRelevancy = ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings)
    results['ResponseRelevancy'] =  await scorerResponseRelevancy.single_turn_ascore(sampleResponseRelevancy)

    # Setup LLM
    # client = AsyncOpenAI()
    # llm = llm_factory("gpt-4o-mini", client=client)

    # # Create metric
    # scorer = Faithfulness(llm=llm)

    # # Evaluate
    # result = await scorer.ascore(
    #     user_input="When was the first super bowl?",
    #     response="The first superbowl was held on Jan 15, 1967",
    #     retrieved_contexts=[
    #         "The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles."
    #     ]
    # )
    # print(f"Faithfulness Score: {result.value}")

    pass
