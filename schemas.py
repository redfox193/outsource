from pydantic import BaseModel, root_validator, model_validator
from typing import Optional
from datetime import date


class ProjectBase(BaseModel):
    name: str
    description: str
    budget: float
    deadline: date


class ProjectCreate(ProjectBase):
    @model_validator(mode='after')
    def check(self):
        if not self.name:
            raise ValueError("Name must be specified.")

        if self.name == 'None':
            raise ValueError("Name must not be 'None'.")

        if not self.description:
            raise ValueError("Description must be specified.")

        if self.budget <= 0:
            raise ValueError("Budget must be greater than 0.")

        if self.deadline <= date.today():
            raise ValueError("Deadline must be greater than the current date.")

        return self


class ProjectUpdate(ProjectBase):
    @model_validator(mode='after')
    def check(self):
        if not self.name:
            raise ValueError("Name must be specified.")

        if self.name == 'None':
            raise ValueError("Name must not be 'None'.")

        if not self.description:
            raise ValueError("Description must be specified.")

        if self.budget <= 0:
            raise ValueError("Budget must be greater than 0.")

        if self.deadline <= date.today():
            raise ValueError("Deadline must be greater than the current date.")

        return self


class Project(ProjectBase):
    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    fullName: str
    position: str
    completedProjects: int
    projectId: Optional[int]


class EmployeeCreate(EmployeeBase):
    @model_validator(mode='after')
    def check(self):
        if not self.fullName:
            raise ValueError("Name must be specified.")

        if not self.position:
            raise ValueError("Position must be specified.")

        if self.completedProjects < 0:
            raise ValueError("Completed projects must be greater or equal 0.")

        return self


class EmployeeUpdate(EmployeeBase):
    @model_validator(mode='after')
    def check(self):
        if not self.fullName:
            raise ValueError("Name must be specified.")

        if not self.position:
            raise ValueError("Position must be specified.")

        if self.completedProjects < 0:
            raise ValueError("Completed projects must be greater or equal 0.")

        return self


class Employee(EmployeeBase):
    class Config:
        from_attributes = True
