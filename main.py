from dotenv import load_dotenv
from fastapi import FastAPI

from app.docs.router import router as docs_router
from app.docs.schemas import SearchToursRequest
from app.vectorstore.mongo_atlas import get_vector_store


# Load env vars from `.env` at startup (OPENAI_API_KEY, MONGODB_URI, etc.)
load_dotenv()

app = FastAPI()


app.include_router(docs_router)

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Search"])

@router.post("/search-tours")
async def search_tours(payload: SearchToursRequest):
    vector_store = get_vector_store()

    docs = vector_store.similarity_search(
        payload.query,
        k=payload.k
    )


    tours = [
        {"content": d.page_content, "metadata": d.metadata}
        for d in docs
    ]

    return {"query": payload.query, "count": len(tours), "tours": tours}


app.include_router(router)



@app.get("/")
def hello_world() -> dict[str, str]:
    return {"message": "Hello World"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)



