
from io import BytesIO

from PIL import Image
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
        student_info = self.studentImageHandler_org(req.studentId)

        student_info.SetInfo('name', str(req.name))
        student_info.SetInfo('email', str(req.email))
        student_info.SetInfo('studentId', str(req.studentId))
        student_info.SetInfo('tawjihiGrade', str(req.tawjihiGrade))
        student_info.SetInfo('Address', str(req.address))
        student_info.SetInfo('govId', str(req.gov_ID))
        student_info.SetInfo('dateOfBirth', str(req.dateOfBirth))
        student_info.SetInfo('phoneNumber', str(req.phoneNumber))
        student_info.SetInfo('status',"Active")
        student_info.SetPassword(str(req.name)+'@'+str(req.studentId), req.studentId)

        image2 = Image.fromarray(student_info.TheImage)

        imagebytes = self.ImageToBlob(image2)

        AdminQueries.updateImg(req.studentId, imagebytes)

        return {200, "success"}

    def add_new_image(self, id: int, img: bytes):
        AdminQueries.createImg(id, None, img)

    def get_student_by_id(self, id):
        student_info = self.studentImageHandler(id)
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

    def get_org_image_by_id(self, studentId):
        student_info = self.studentImageHandler_org(studentId)
        image2 = Image.fromarray(student_info.TheImage)
        image2.thumbnail((200,200))
        image3 = self.ImageToBlob(image2)
        return image3

    def deactivate_student(self,student_id:int):
        student_info = self.studentImageHandler(student_id)
        if not student_info:
            return False
        student_info.SetInfo("status","Deactivated")
        image = Image.fromarray(student_info.TheImage)
        imagebytes = self.ImageToBlob(image)
        AdminQueries.updateImg(student_id, imagebytes)
        return True

    def activate_student(self,student_id:int):
        student_info = self.studentImageHandler(student_id)
        if not student_info:
            return False
        student_info.SetInfo("status","active")
        image = Image.fromarray(student_info.TheImage)
        imagebytes = self.ImageToBlob(image)
        AdminQueries.updateImg(student_id, imagebytes)
        return True

    def check_students_limit(self,offset):
        number_of_students = AdminQueries.image_count()
        if offset > number_of_students[0]:
            return False
        return True

    def get_students(self,page,page_size):
        offset = (page-1) * page_size
        check = self.check_students_limit(offset)
        if not check:
            return None
        images = AdminQueries.get_images(offset,page_size)
        result =[]
        for img in images:
            info = self.get_student_by_id(int(img[0]))
            resp = AllStudentsResponse()
            resp.id = info["studentId"]
            resp.name = info["name"]
            resp.email = info["email"]
            resp.status = info["status"]
            resp.image = f"/admin/students/{img[0]}/image"
            result.append(resp)
        return result

    def store_transcript(self,transcript, id):
        student_image = self.studentImageHandler_org(id)
        student_info = self.get_student_by_id(id)
        for info in student_info:
            student_image.SetInfo(info, student_info[info])
        student_image.AddTranscript(transcript, id)
        image = Image.fromarray(student_image.TheImage)
        image_bytes = self.ImageToBlob(image)
        AdminQueries.updateImg(id, image_bytes)

    def read_transcript(self, id):
        student_info = self.studentImageHandler(id)
        transcript = student_info.TranscriptRead(id)
        return transcript











class AdminQueries:
    @staticmethod
    def createImg(id, img=None, img_org=None):
        query = "insert into Images (id,image,image_org) values (?,?,?)"
        result = execute(query, (str(id), img, img_org), True)
        return result

    @staticmethod
    def get_images(offset, page_size):
        query = "select * from Images limit ? offset ?"
        result = execute(query, (page_size, offset))
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
    def deleteImg(id):
        query = "delete from Images where id=?"
        result = execute(query, (str(id),))
        return result

    @staticmethod
    def image_count():
        query = "select count(image) from Images"
        result = execute(query, None, True)
        return result