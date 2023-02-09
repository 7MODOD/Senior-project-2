import uvicorn as uvicorn
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from fastapi.responses import JSONResponse
from starlette.responses import Response

import admin
from models.UserRequests import *
from ImageData import ImageData
from StudentImage import StudentImage
import pics
import sqlite3

app = FastAPI()

conn = sqlite3.connect('IMAGES.db')
#cursor = conn.cursor()

#cursor.execute("create table Images(id integer primary key, image BLOB)")
#cursor.execute("select * from Images")
#result = cursor.fetchall()
#print(result)

"""
@app.get(
    "/image",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response,
)
def get_image():
    conn = sqlite3.connect('IMAGES.db')
    qur = "select Image from Images where id = 201812169"
    curs = conn.cursor()

    result = curs.execute(qur).fetchone()
    image_bytes: bytes = result[0]
    # media_type here sets the media type of the actual response sent to the client.
    return Response(content=[image_bytes,image_bytes,image_bytes], media_type="image/png")

@app.get('/')
def homePage():
    return {"home"}

@app.post('/admin')
def adminLogin(req: UserLogin):
    conn = sqlite3.connect('IMAGES.db')
    cursor = conn.cursor()
    cursor.execute('''select image from Images where id = ?''',(req.username, ))
    info = cursor.fetchone()
    myImg = Image.open(info)

    if info is not None:
        stImg = ImageData()
        stInfo = stImg.getTheInformationNames(req.username)
        student = StudentImage(info, stInfo)
        password = student.GetInfo("password")
        if req.password == password:
            result = student.GetStudentInformation()
            return {result, myImg.thumbnail(200, 200)}
        else:
            return {None}
    else:
        return {None}






def getCurrentUser(token:str):
    token1 = token.split(':')
    username = token1[0]
    password = token1[1]

    return
@app.get('/users/{userId}')
def userLogin(userId: int):

    return






import sys
import numpy as np
from PIL import Image
from ImageData import ImageData
from StudentImage import StudentImage


# You can edit those to add more attributes to be added to the image.
# Note : Select a second arguments that does not exist already.
array = []
array.append(ImageData("Name", 5))
array.append(ImageData("Email Address", 17))
array.append(ImageData("University ID", 23))
array.append(ImageData("GPA", 124))
array.append(ImageData("Tawjihi grade", 78))
array.append(ImageData("Address", 1010))
array.append(ImageData("ID number", 123))
array.append(ImageData("Date of birth", 646))
array.append(ImageData("Phone number", 51))
array.append(ImageData("Student academic status", 864))



# The types of data we can edit in the picture :
# Note: U need to set the data at least once for each picture before u can read it.
        #  "D:/ProfilePictures/201812451.png"
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

    # Read The Picture

img = StudentImage("D:/image3.jpg",array)
img.SetInfo("Name", "Yousef")
img.SetInfo("Email Address", "Yousef@gmail.com")
img.SetInfo("University ID", "201812169")
img.SetInfo("GPA", "2.54")
img.SetInfo("Tawjihi grade", "95.5")
img.SetInfo("Address", "jenin_aaup")
img.SetInfo("ID number", "374821461")
img.SetInfo("Date of birth", "22-12-2022")
img.SetInfo("Student academic status", "active")
img.SetInfo("Phone number", "+970597876548")





print(img.GetInfo("Name"))
print(img.GetInfo("GPA"))
print(img.GetInfo("Phone number"))
print(img.GetStudentInformation())

"""

stImg = ImageData()
stInfo = stImg.getTheInformationNames("201812169")
ad = admin.AdminComponent()
img = ad.studentImageHandler_org(201812169)

img.SetInfo("Name", "Yousef")
img.SetInfo("University ID", "201812169")
img.SetInfo("Email Address", "Yousef@gmail.com")
path = "C:/Users/od7mo/OneDrive/Desktop/py_senior/Senior-project-2/transcript.csv"
img.AddTranscript(path, 201812169)
print(img.TranscriptRead(201812169))
print(img.GetInfo("University ID"))

#if __name__ == "__main__":
#    uvicorn.run(app, port=8000)
