"""
Database models and configuration for the High School Management System
"""

from sqlalchemy import create_engine, Column, String, Integer, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pathlib import Path
import os

# Database setup
DATABASE_URL = "sqlite:///./school_activities.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association table for many-to-many relationship between activities and participants
activity_participants = Table(
    'activity_participants',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id')),
    Column('participant_id', Integer, ForeignKey('participants.id'))
)

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)
    
    # Many-to-many relationship with participants
    participants = relationship("Participant", secondary=activity_participants, back_populates="activities")

class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Many-to-many relationship with activities
    activities = relationship("Activity", secondary=activity_participants, back_populates="participants")

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_sample_data(db: Session):
    """Initialize database with sample activities if it's empty"""
    # Check if we already have activities
    if db.query(Activity).first() is not None:
        return
    
    # Sample activities data
    sample_activities = [
        {
            "name": "Chess Club",
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        {
            "name": "Programming Class",
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        {
            "name": "Gym Class",
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        {
            "name": "Soccer Team",
            "description": "Join the school soccer team and compete in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        {
            "name": "Basketball Team",
            "description": "Practice and play basketball with the school team",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        {
            "name": "Art Club",
            "description": "Explore your creativity through painting and drawing",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
        },
        {
            "name": "Drama Club",
            "description": "Act, direct, and produce plays and performances",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
        },
        {
            "name": "Math Club",
            "description": "Solve challenging problems and participate in math competitions",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
        },
        {
            "name": "Debate Team",
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
        }
    ]
    
    for activity_data in sample_activities:
        # Create activity
        activity = Activity(
            name=activity_data["name"],
            description=activity_data["description"],
            schedule=activity_data["schedule"],
            max_participants=activity_data["max_participants"]
        )
        db.add(activity)
        db.flush()  # Flush to get the ID
        
        # Create participants and associate with activity
        for email in activity_data["participants"]:
            # Check if participant already exists
            participant = db.query(Participant).filter(Participant.email == email).first()
            if not participant:
                participant = Participant(email=email)
                db.add(participant)
                db.flush()
            
            # Associate participant with activity
            activity.participants.append(participant)
    
    db.commit()
