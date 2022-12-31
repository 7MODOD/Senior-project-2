class ImageData():

    def __init__(self):

        self.list = ["name","email","studentId", "tawjihiGrade",
                     "Address","govId","dateOfBirth",
                     "phoneNumber","status"]

    def getTheInformationNames(self,number):
        key = int(number) % 10
        if key==0:
            print()
        dec = {}
        for i, j in zip(range(100, 200, key), self.list):
            dec[j] = i
        return dec

"""
i have a transcript of 100 course and 100 mark
so i need 300 column at minimum to store course name, mark, and number of character of the name

where should i store the places?? 




"""