
from io import BytesIO

from PIL import Image
import numpy as np
from StudentImage import StudentImage
from models.dbModel import *
from models.UserRequests import *
from ImageData import *
class AdminComponent:

    def studentImageHandler_org(self, id):
        image = AdminQueries.getImg_org(id)
        image_bytes = BytesIO(image[0])
        img_data = ImageData()
        array = img_data.getTheInformationNames(id)
        student_info = StudentImage(image_bytes, array)
        return student_info

    def studentImageHandler(self, id):
        image = AdminQueries.getImage(id)
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


    def checkStudent(self, id):
        result = AdminQueries.getImg_org(id)
        if not result:
            return False

        return True

    def add_new_student(self, req: Createuser):
        student_info = self.studentImageHandler(req.studentId)


        student_info.SetInfo('name', str(req.name))
        student_info.SetInfo('email', str(req.email))
        student_info.SetInfo('studentId', str(req.studentId))
        student_info.SetInfo('tawjihiGrade', str(req.tawjihiGrade))
        student_info.SetInfo('Address', str(req.address))
        student_info.SetInfo('govId', str(req.gov_ID))
        student_info.SetInfo('dateOfBirth', str(req.dateOfBirth))
        student_info.SetInfo('phoneNumber', str(req.phoneNumber))
        student_info.SetInfo('status',"Active")

        image2 = Image.fromarray(student_info.TheImage)

        imagebytes = self.ImageToBlob(image2)

        AdminQueries.updateImg(req.studentId, imagebytes)

        return {200, "success"}

    def get_student_by_id(self, id):
        image = AdminQueries.getImage(id)
        image_bytes = BytesIO(image[0])
        img_data = ImageData()
        array = img_data.getTheInformationNames(id)
        student_info = StudentImage(image_bytes, array)

        result = student_info.GetStudentInformation()

        return result

    def update_student_by_admin(self, req, id):
        student_info = self.studentImageHandler(id)

        for item in vars(req):
            if not getattr(req,item):
                continue
            student_info.SetInfo(item, getattr(req, item))

        image = Image.fromarray(student_info.TheImage)
        imagebytes = self.ImageToBlob(image)

        AdminQueries.updateImg(id, imagebytes)
        return True









class AdminQueries:
    @staticmethod
    def createImg(id, img=None, img_org=None):
        query = "insert into Images (id,image,image_org) values (?,?,?)"
        result = execute(query, (str(id), img, img_org), True)
        return result

    @staticmethod
    def getImages( page, page_size):
        offset = page*page_size
        query = "select image from Images offset=? limit= ?"
        result = execute(query, (offset, page_size))
        return result

    @staticmethod
    def getImage(id):
        query = "select image from Images where id=?"
        result = execute(query,(id,), True)
        return result

    @staticmethod
    def getImg_org(id):
        query = "select image_org from Images where id=?"
        result = execute(query, (str(id),), True)
        return result

    @staticmethod
    def updateImg(id, img, img_org=None):
        if img_org is None:
            query = "update Images set image= ? where id=?"
            result = execute(query, (img, str(id)))
        else:
            query = "update Images set image=? , image_org=? where id=?"
            result = execute(query, (img, img_org, str(id)))


        return result

    @staticmethod
    def deleteImg( id):
        query = "delete from Images where id=?"
        result = execute(query, (str(id),))
        return result
