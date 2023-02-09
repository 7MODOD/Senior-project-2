from click import DateTime
from pydantic import BaseModel

class UserLogin(BaseModel):
    studentId: int
    password: str


class Createuser(BaseModel):
    studentId: int
    name: str
    email: str
    #studentGPA: float
    tawjihiGrade: float
    address: str
    govId: int
    dateOfBirth: str
    #status: str
    phoneNumber: str
    password: str | None = 0


class Updateuser_byAdmin(BaseModel):
    name: str | None = None
    email: str | None = None
    tawjihiGrade: float | None = None
    address: str | None = None
    govId: int | None = None
    dateOfBirth: str | None = None
    phoneNumber: str | None = None


class UserUpdate(BaseModel):
    password: str | None = None
    phoneNumber: str | None = None

class AllStudentsResponse():
    studentId: int
    name: str | None = ""
    email: str | None = ""
    status: str
    image: str | None = ""

'''
["Name","Email Address","University ID", "Tawjihi grade",
                     "Address","Gov Id","Date of birth",
                     "Phone number","Student academic status"]
'''





# Name.
        # Email address.
        # University ID.
        # GPA.
        # Tawjihi grade.
        # Address.
        # ID number.
        # Date of birth.
        # Student academic status.
        # Phone number.