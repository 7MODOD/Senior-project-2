from io import BytesIO

from PIL import Image
from StudentImage import StudentImage
from models.dbModel import *
from models.UserRequests import *
from ImageData import *


class StudentComponent:

    def studentImageHandler(self, id):
        image = StudentQueries.getImage(id)
        image_bytes = BytesIO(image[0])
        img_data = ImageData()
        array = img_data.getTheInformationNames(id)
        student_info = StudentImage(image_bytes, array)
        return student_info

    def ImageToBlob(self,image):
        stream = BytesIO()
        image.save(stream, format="PNG")
        imagebytes = stream.getvalue()
        return imagebytes


    def authorization(self,student_id:str, password:str):
        exist = StudentQueries.getImg(student_id)
        if not exist:
            return False
        student_image = self.studentImageHandler(student_id)
        passw = str(student_image.ReadPassword(int(student_id)))
        return password == passw

    def get_student_info(self,student_id):
        student_image = self.studentImageHandler(student_id)
        student_info = student_image.GetStudentInformation()
        return student_info

    def get_student_transcript(self, student_id):
        student_image = self.studentImageHandler(id)
        transcript = student_image.TranscriptRead(id)
        return transcript

"""
    def checkStudent(self, id):
        result = StudentQueries.getImg(id)
        if not result:
            return False
        return True


    def login(self,req:UserLogin):
        student_image = self.studentImageHandler(req.username)
        password = student_image.ReadPassword(req.username)
        return req.password == password
"""



class StudentQueries:

    @staticmethod
    def getImage(id):
        query = "select image from Images where id=?"
        result = execute(query, (id,), True)
        return result