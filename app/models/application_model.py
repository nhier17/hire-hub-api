from .. import db
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from datetime import datetime, timezone

class Application(db.Model):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    date_applied = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    cover_letter = Column(Text, nullable=True)

    # Relationships
    user = db.relationship('User', back_populates='applications')
    job = db.relationship('Job', back_populates='applications')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "date_applied": self.date_applied.isoformat(),
            "cover_letter": self.cover_letter,
        }
