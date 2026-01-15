from dotenv import load_dotenv
from fastapi import FastAPI

from app.docs.router import router as docs_router


# Load env vars from `.env` at startup (OPENAI_API_KEY, MONGODB_URI, etc.)
load_dotenv()

app = FastAPI()


app.include_router(docs_router)


@app.get("/")
def hello_world() -> dict[str, str]:
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
