from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
import shutil
import uuid
import time

from src.memory.memory_store import MemoryStore
from src.evaluation.rag_eval import RAGEvaluator

from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.image_search import ImageSearcher
from src.pipelines.sql_pipeline import SQLPipeline


app = FastAPI(title="Multimodal RAG System")

UPLOAD_DIR = Path("tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

memory_store = MemoryStore(max_messages=5)
evaluator = RAGEvaluator()
sql_pipeline = SQLPipeline()

hybrid_retriever = HybridRetriever(top_k=5)
image_searcher = ImageSearcher(top_k=5)


def build_response(answer, context, scores, trace_id):
    return {
        "trace_id": trace_id,
        "answer": answer,
        "context_used": context,
        "evaluation": scores,
        "timestamp": time.time()
    }


def serialize_context(context):
    cleaned = []

    for c in context:
        cleaned.append({
            "text": c.get("text"),
            "score": float(c.get("score", 0.0)),
            "retrieval_type": c.get("retrieval_type"),
            "metadata": c.get("metadata", {})
        })

    return cleaned


def normalize_image_context(context):
    normalized = []

    for c in context:
        if c.get("caption"):
            normalized.append({"text": c["caption"]})
        if c.get("ocr_text"):
            normalized.append({"text": c["ocr_text"]})

    return normalized


@app.post("/ask")
def ask(question: str):
    trace_id = str(uuid.uuid4())

    retrieved_chunks = hybrid_retriever.hybrid_search(question)

    result = {
        "answer": retrieved_chunks[0]["text"] if retrieved_chunks else "",
        "context": retrieved_chunks
    }

    refined_answer = evaluator.refine_answer(
        question,
        result["answer"],
        result["context"]
    )

    raw_scores = evaluator.evaluate(
        refined_answer,
        result["context"]
    )

    scores = {
        "faithfulness": raw_scores.get("faithfulness"),
        "confidence": raw_scores.get("confidence"),
        "hallucination_risk": raw_scores.get("hallucination_risk")
    }

    memory_store.add_message(question, refined_answer)

    return build_response(
        refined_answer,
        serialize_context(result["context"]),
        scores,
        trace_id
    )



@app.post("/ask-image")
def ask_image(
    question: str = Form(None),
    image: UploadFile = File(None),
):
    trace_id=str(uuid.uuid4())

    if not question and not image:
        return {"error":"Provide text or image"}

    if question and not image:
        results=image_searcher.search_by_text(question)

        memory_store.add_message(question,f"Returned {len(results)} images")

        return {
            "trace_id":trace_id,
            "answer":"Images retrieved from text query",
            "context_used":results,
            "timestamp":time.time()
        }

    image_path=UPLOAD_DIR/f"{uuid.uuid4()}_{image.filename}"
    with open(image_path,"wb") as f:
        shutil.copyfileobj(image.file,f)

    texts=image_searcher.image_to_text(str(image_path))

    answer=" | ".join(
        t.replace("\n"," ").strip()
        for t in texts
    ) if texts else "No text could be extracted from the image."

    scores=evaluator.evaluate(answer,[{"text":t} for t in texts])

    memory_store.add_message("image_to_text",answer)

    return build_response(
        answer,
        [],
        {
            "faithfulness":scores.get("faithfulness"),
            "confidence":scores.get("confidence"),
            "hallucination_risk":scores.get("hallucination_risk")
        },
        trace_id
    )



@app.post("/ask-image-image")
def ask_image_image(
    image: UploadFile = File(...),
):
    trace_id = str(uuid.uuid4())

    image_path = UPLOAD_DIR / f"{uuid.uuid4()}_{image.filename}"
    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    results = image_searcher.search_by_image(str(image_path))

    memory_store.add_message("image_to_image", f"Returned {len(results)} images")

    return {
        "trace_id": trace_id,
        "answer": "Similar images found",
        "context_used": results,
        "timestamp": time.time()
    }


@app.post("/ask-sql")
def ask_sql(question: str):
    trace_id = str(uuid.uuid4())

    result = sql_pipeline.run(question)

    memory_store.add_message(question, str(result))

    return {
        "trace_id": trace_id,
        "answer": str(result),
        "timestamp": time.time()
    }
