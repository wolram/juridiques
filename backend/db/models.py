# Database Models (SQLAlchemy)

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # None se usar OAuth
    full_name = Column(String(255))
    oab_number = Column(String(50), nullable=True)  # número da OAB
    role = Column(String(50), default="user")  # "user", "admin", "jurist"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    threads = relationship("Thread", back_populates="owner")
    spaces = relationship("Space", back_populates="owner")
    audit_logs = relationship("AuditLog", back_populates="user")


class Space(Base):
    __tablename__ = "spaces"
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)  # "Banco X - B&A", "Crédito SP", etc.
    description = Column(Text)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="spaces")
    threads = relationship("Thread", back_populates="space")
    processes = relationship("Process", back_populates="space")


class Thread(Base):
    __tablename__ = "threads"
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=True)
    title = Column(String(255), nullable=False)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=True)
    status = Column(String(50), default="draft")  # "draft", "active", "closed"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="threads")
    space = relationship("Space", back_populates="threads")
    messages = relationship("Message", back_populates="thread")
    process = relationship("Process", back_populates="threads")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey("threads.id"), nullable=False)
    role = Column(String(50))  # "user", "assistant"
    content = Column(Text)
    metadata = Column(JSON)  # {sources: [...], confidence: 0.8, ...}
    created_at = Column(DateTime, default=datetime.utcnow)
    
    thread = relationship("Thread", back_populates="messages")


class Process(Base):
    __tablename__ = "processes"
    
    id = Column(Integer, primary_key=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False)
    cnj_number = Column(String(50), unique=True, nullable=True)
    tribunal = Column(String(255))
    classe = Column(String(255))
    partes = Column(Text)  # "fulano x sicrano"
    status = Column(String(50), default="pending")  # "pending", "active", "concluded"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    space = relationship("Space", back_populates="processes")
    threads = relationship("Thread", back_populates="process")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(255))  # "create_thread", "run_agent", "export_pdf", etc.
    resource_type = Column(String(50))  # "thread", "process", "agent"
    resource_id = Column(Integer)
    details = Column(JSON)  # {input_hash, output_summary, agent_used, ...}
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="audit_logs")
