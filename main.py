import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import NewsPost, Review, Horse, TeamMember, ContactMessage, BookingRequest, FaqItem

app = FastAPI(title="Táltos Lovasudvar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Táltos Lovasudvar Backend Running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "collections": [],
    }

    try:
        if db is not None:
            response["database"] = "✅ Connected"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:20]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:120]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"

    return response


# Helper to convert Mongo documents
class MongoEncoder(BaseModel):
    id: str


def encode_doc(doc: dict):
    if not doc:
        return doc
    doc["id"] = str(doc.get("_id"))
    doc.pop("_id", None)
    return doc


# Public endpoints used by the site
@app.get("/api/news")
def list_news(lang: Optional[str] = None, limit: int = 4):
    filt = {"lang": lang} if lang else {}
    docs = get_documents("newspost", filt, limit)
    # Return raw fields; client maps as needed
    return [encode_doc(d) for d in docs]


@app.post("/api/contact")
def submit_contact(payload: ContactMessage):
    doc_id = create_document("contactmessage", payload)
    return {"ok": True, "id": doc_id}


@app.post("/api/booking")
def submit_booking(payload: BookingRequest):
    doc_id = create_document("bookingrequest", payload)
    return {"ok": True, "id": doc_id, "message": "Köszönjük! 48 órán belül válaszolunk."}


@app.get("/api/horses")
def list_horses(limit: int = 50):
    docs = get_documents("horse", {}, limit)
    return [encode_doc(d) for d in docs]


@app.get("/api/reviews")
def list_reviews(lang: Optional[str] = None, limit: int = 10):
    filt = {"lang": lang} if lang else {}
    docs = get_documents("review", filt, limit)
    return [encode_doc(d) for d in docs]


@app.get("/schema")
def get_schema_info():
    return {
        "collections": [
            "newspost",
            "review",
            "horse",
            "teammember",
            "contactmessage",
            "bookingrequest",
            "faqitem",
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
