from .. import db
from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime
from datetime import datetime, timezone

class Application(db.Model):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    phone_number = Column(String(20), nullable=False) 
    resume = Column(String(255), nullable=False)  
    portfolio = Column(String(255), nullable=True)  
    country_of_residence = Column(String(100), nullable=False)
    notice_period = Column(Integer, nullable=False)  
    salary_expectation = Column(Integer, nullable=False)  
    years_of_experience = Column(Integer, nullable=False)
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
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "resume": self.resume,
            "portfolio": self.portfolio,
            "country_of_residence": self.country_of_residence,
            "notice_period": self.notice_period,
            "salary_expectation": self.salary_expectation,
            "years_of_experience": self.years_of_experience,
            "date_applied": self.date_applied.isoformat(),
            "cover_letter": self.cover_letter,
        }
