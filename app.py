import uvicorn as uvicorn
from fastapi import FastAPI, File, UploadFile,Request,Response

from admin import AdminComponent
from models.dbModel import *
from PIL import Image
from fastapi.responses import JSONResponse
from starlette.responses import Response

from models.UserRequests import *
from ImageData import ImageData
from StudentImage import StudentImage
import pics
import sqlite3

#post /admin/students/{ID_NUMBER}
app = FastAPI()

@app.post('/admin/students/id_number/img')
@app.post('/admin/students/')
def createuser(req: Createuser):
    admin = AdminComponent()
    exist = admin.checkStudent(req.studentId)
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)

    admin.add_new_student(req)

    return JSONResponse({"status":"SUCCESS"},status_code=200)

@app.get('/admin/students/{student_id}')
def getstudent(student_id:int):
    admin = AdminComponent()
    exist = admin.checkStudent(str(student_id))
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)

    result = admin.get_student_by_id(str(student_id))
    return JSONResponse({"student information": result},status_code=200)

@app.put('/admin/students/{student_id}')
def updatestudent(req: Updateuser_byAdmin, student_id: int):
    admin = AdminComponent()
    exist = admin.checkStudent(str(student_id))
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)

    response = admin.update_student_by_admin(req,student_id)
    if response is True:
        return JSONResponse({"status": "info was updated"}, status_code=200)

    return JSONResponse({"status": "at least one field should be filled"}, status_code=400)


@app.get('/admin/students/{student_id}/image', responses= {
                            200: {"content": {"image/png": {}}}})
def getOrgImage(student_id: int):
    admin = AdminComponent()
    exist = admin.checkStudent(str(student_id))
    if not exist:
        return JSONResponse({"status": "insert the image first"}, status_code=400)
    result = admin.get_org_image_by_id(student_id)

    return Response(content=result, media_type="image/png")

#PUT /admin/students/{ID_NUMBER}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)