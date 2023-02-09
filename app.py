import uvicorn as uvicorn
from fastapi import FastAPI, File, UploadFile, Request, Response, Body

from admin import AdminComponent
from models.dbModel import *
from PIL import Image
from fastapi.responses import JSONResponse
from starlette.responses import Response

from models.UserRequests import *
from ImageData import ImageData
from StudentImage import StudentImage

from fastapi.middleware.cors import CORSMiddleware

from student import StudentComponent

#post /admin/students/{student_id}
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/admin/students/{student_id}/image')
def send_user_image(image: UploadFile, student_id: int):
    admin = AdminComponent()
    exist = admin.checkStudent(student_id)
    if exist:
        return JSONResponse({"status": "this student is exist"}, status_code=400)
    admin.add_new_image(student_id, image.file)
    return JSONResponse({"status": "SUCCESS"}, status_code=200)


@app.post('/admin/students/')
def createuser(req: Createuser):
    admin = AdminComponent()
    exist = admin.checkStudent(req.studentId)
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)

    admin.add_new_student(req)

    return JSONResponse({"status": "SUCCESS"}, status_code=200)


@app.get('/admin/students/{student_id}')
def getstudent(student_id: int):
    admin = AdminComponent()
    exist = admin.checkStudent(str(student_id))
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)

    result = admin.get_student_by_id(str(student_id))
    return JSONResponse({"student information": result}, status_code=200)


@app.put('/admin/students/{student_id}')
def updatestudent(req: Updateuser_byAdmin, student_id: int):
    admin = AdminComponent()
    exist = admin.checkStudent(str(student_id))
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)

    response = admin.update_student_by_admin(req, student_id)
    if response is True:
        return JSONResponse({"status": "info was updated"}, status_code=200)

    return JSONResponse({"status": "at least one field should be filled"}, status_code=400)


@app.get('/admin/students/{student_id}/image', responses={
    200: {"content": {"image/png": {}}}})
def getOrgImage(student_id: int):
    admin = AdminComponent()
    exist = admin.checkStudent(str(student_id))
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)
    result = admin.get_org_image_by_id(student_id)

    return Response(content=result, media_type="image/png")


@app.post("/admin/students/{student_id}/deactivate")
def deactivate_student(student_id: int):
    admin = AdminComponent()
    exist = admin.checkStudent(str(student_id))
    if not exist:
        return JSONResponse({"status": f"there is no student with this student_id {student_id}...pls try again"}, status_code=400)
    response = admin.deactivate_student(student_id)
    if response is True:
        return JSONResponse({"status": "student was deactivated"}, status_code=200)

    return JSONResponse({"status": "this student has no information yet"}, status_code=400)


@app.post("/admin/students/{student_id}/activate")
def deactivate_student(student_id: int):
    admin = AdminComponent()
    exist = admin.checkStudent(str(student_id))
    if not exist:
        return JSONResponse({"status": f"there is no student with this student_id {student_id}...pls try again"}, status_code=400)
    response = admin.activate_student(student_id)
    if response is True:
        return JSONResponse({"status": "student was activated"}, status_code=200)

    return JSONResponse({"status": "this student has no information yet"}, status_code=400)


@app.get("/admin/students")
def get_students(page_number: int = 1, page_size: int = 10):
    admin = AdminComponent()
    resp = admin.get_students(page_number, page_size)
    if not resp:
        return JSONResponse({"students information": "the number of student is less than you request"}, status_code=400)
    return {"students information": resp, }


@app.post("/admin/students/{student_id}/transcript")
def add_transcript(student_id, files: UploadFile):
    admin = AdminComponent()
    exist = admin.checkStudent(student_id)
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)

    admin.store_transcript(files, student_id)

    return JSONResponse({"status": "SUCCESS"}, status_code=200)


@app.get("/admin/students/{student_id}/transcript")
def get_student_transcript(student_id):
    admin = AdminComponent()
    exist = admin.checkStudent(str(student_id))
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)

    result = admin.read_transcript(student_id)
    return JSONResponse({"student information": result}, status_code=200)

# after this comment the student APIs starts ><<><><>><<>><<<<<<<<<<<<<<<<<<<<<<><><><><><><><><><<>><<>><<>><><><><<>


@app.post("/login")
def student_login(req: UserLogin):
    student = StudentComponent()
    authenticate = student.authorization(str(req.studentId), req.password)
    if not authenticate:
        return JSONResponse({"status": "the username or password is wrong"}, status_code=400)

    return JSONResponse({"Authorization": f"{req.studentId}@{req.password}"}, status_code=200)


@app.get("/students")
def get_info_for_student(req: Request):
    student_id, password = req.headers.get("Authorization").split('@')
    student = StudentComponent()
    authorized = student.authorization(student_id, password)
    if not authorized:
        return JSONResponse({"status": "you are not authorized"}, status_code=400)
    result = student.get_student_info(student_id)
    return JSONResponse({"student information": result}, status_code=200)


@app.get("/students/transcript")
def get_transcript_for_student(req: Request):
    student_id, password = req.headers.get("Authorization").split('@')
    student = StudentComponent()
    authorized = student.authorization(student_id, password)
    if not authorized:
        return JSONResponse({"status": "you are not authorized"}, status_code=400)
    result = student.get_student_transcript(student_id)
    return JSONResponse({"student information": result}, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
