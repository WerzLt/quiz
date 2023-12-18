import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# SQL Table
engine = create_engine('sqlite:///quiz_game.db')
Base = declarative_base()

# Tables Creation
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

class Level(Base):
    __tablename__ = 'levels'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    level_id = Column(Integer, ForeignKey('levels.id'), nullable=False)
    question_type = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    answers = relationship('Answer', back_populates='question')
    question_answers = relationship('Answers', back_populates='question')

    def __repr__(self):
        return f"{self.id} Lygis: {self.level_id} \nKlausimas: {self.text}"

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    correct_answer = Column(String, nullable=False)
    question = relationship('Question', back_populates='answers')

    def __repr__(self):
        return f"ID: {self.id} Klausimo id: {self.question_id} Atsakymas: {self.correct_answer}"

class Answers(Base):
    __tablename__ = 'question_answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    answers = Column(String, nullable=False)
    question = relationship('Question', back_populates='question_answers')

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_username = Column(String, nullable=False)
    level_id = Column(Integer, ForeignKey('levels.id'), nullable=False)
    score = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"ID: {self.user_id} Vardas: {self.user_username} Lygis: {self.level_id} Taškai: {self.score} {self.data} "

if __name__ == "__main__":
    Base.metadata.create_all(engine)