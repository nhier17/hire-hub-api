from . import db
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone

class Job(db.Model):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    date_posted = Column(DateTime, default=lambda: datetime.now(timezone.utc)) 
    salary = Column(String(50))
    employment_type = Column(String(50))
    application_deadline = Column(DateTime)
    skills_required = Column(String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'salary': self.salary,
            'employment_type': self.employment_type,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'skills_required': self.skills_required,
            'date_posted': self.date_posted.isoformat()  # Ensure ISO format for datetime
        }

    def from_dict(self, data):
        for field in ['title', 'company', 'location', 'description']:
            if field in data:
                setattr(self, field, data[field])
