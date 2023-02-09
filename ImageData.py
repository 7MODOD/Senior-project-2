class ImageData():

    def __init__(self):

        self.list = ["name","email","studentId", "tawjihiGrade",
                     "address","govId","dateOfBirth",
                     "phoneNumber","status"]

    def getTheInformationNames(self,number):
        key = int(number) % 10
        if key==0:
            print()
        dec = {}
        for i, j in zip(range(100, 200, key), self.list):
            dec[j] = i
        return dec
    @staticmethod
    def get_transcript_location(number):
        transcript_location = (int(number) % 10) + 200
        return transcript_location

    @staticmethod
    def get_password_location(number):
        password_location = (int(number) % 100) + 300
        return password_location

"""
i have a transcript of 100 course and 100 mark
so i need 300 column at minimum to store course name, mark, and number of character of the name

where should i store the places?? 




"""