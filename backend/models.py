from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class AgentRunRequest(BaseModel):
    input: str
    thread_id: Optional[str] = None
    space_id: Optional[str] = None
    user_id: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


class Citation(BaseModel):
    type: str
    ref: str
    link: Optional[str]


class Section(BaseModel):
    name: str
    text: str
    citations: Optional[List[Citation]] = []


class AgentRunResponse(BaseModel):
    title: Optional[str]
    sections: Optional[List[Section]] = []
    results: Optional[List[Dict[str, Any]]] = None
    metrics: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
