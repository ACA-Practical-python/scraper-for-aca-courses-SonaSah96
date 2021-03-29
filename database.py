from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///lesson_and_tutor.db")
Base = declarative_base()


class Lesson(Base):
    __tablename__ = "lessons"
    lesson_id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False)
    course_id = Column(String, nullable=False, unique=True)
    course_url = Column(String, nullable=False)
    price = Column(String)
    level = Column(String)
    tutors = relationship("Tutor")


class Tutor(Base):
    __tablename__ = "tutors"
    tutor_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    company = Column(String)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id"))


metadata = Base.metadata

if __name__ == "__main__":
    metadata.create_all(bind=engine)
