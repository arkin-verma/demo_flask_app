from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.engine import create_engine
from datetime import datetime

DATABASE_PATH = 'sqlite:///project.sqlite'
Base = declarative_base()

# orm model for the database
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'
    
    def __str__(self) -> str:
        return self.name

class ReviewData(Base):
    __tablename__ = 'review_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_url = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<ReviewData {self.product_url}>' 
    
    def __str__(self) -> str:
        return self.filepath


if __name__ == '__main__':
    engine = create_engine(DATABASE_PATH, echo=True)
    Base.metadata.create_all(engine)
    print(User.__table__)
    print(ReviewData.__table__)