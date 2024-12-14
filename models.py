from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from database import Base


class Project(Base):
    __tablename__ = "Project"
    __table_args__ = {"schema": "outsource"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    budget = Column(DECIMAL(15, 2), nullable=False)
    deadline = Column(Date, nullable=False)
    employees = relationship("Employee", back_populates="project")


class Employee(Base):
    __tablename__ = "Employee"
    __table_args__ = {"schema": "outsource"}

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    completedProjects = Column(Integer, nullable=False, default=0)
    projectId = Column(Integer, ForeignKey("outsource.Project.id"))
    project = relationship("Project", back_populates="employees")
