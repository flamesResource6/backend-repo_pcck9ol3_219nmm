"""
Database Schemas for Táltos Lovasudvar

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercased class name (e.g., NewsPost -> "newspost").
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Core content models
class NewsPost(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    body: str
    lang: str = Field(..., description="Language code: hu, en, de, ro")
    cover_url: Optional[str] = None
    tags: List[str] = []
    published_at: Optional[datetime] = None
    featured: bool = False

class Review(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    lang: str = "hu"
    source: Optional[str] = None  # e.g., Google, Facebook

class Horse(BaseModel):
    name: str
    breed: Optional[str] = None
    age: Optional[int] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    temperament: Optional[str] = None

class TeamMember(BaseModel):
    name: str
    role: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None

# Inquiries and bookings
class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str
    lang: str = "hu"

class BookingRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    lang: str = "hu"
    date: str = Field(..., description="Requested date (ISO or free text)")
    group_size: int = Field(..., ge=1, le=50)
    program: str = Field(..., description="Requested program description")
    notes: Optional[str] = None

# Optional structured FAQ item
class FaqItem(BaseModel):
    category: str
    question: str
    answer: str
    lang: str = "hu"
