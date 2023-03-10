import csv

from PIL import Image
import numpy as np

from ImageData import ImageData
from models.UserRequests import Createuser
class StudentImage():

    def __init__(self, image, array: dict):
        self.TheImage = np.array(Image.open(image))

        self.array = array
    # Save the changes of the image after editing.

    def Save(self):
        img = Image.fromarray(self.TheImage)
        #img.save(image)

    # Add The count of the characters to the image as binary
    def AddCharacterCountToImage(self, BinaryArray, LineNumber):
        index = 0
        for x in range(0, len(BinaryArray)):
            self.TheImage[LineNumber][-(8-x)] = self.AddBitToPixel(self.TheImage[LineNumber]

                                                                   [len(self.TheImage) - len(BinaryArray) + x], index, BinaryArray[x])

    # Read The Number of characters for the data in this row
    def ReadCharacterCount(self, LineNumber):
        value = ""
        for x in range(0, 8):
            value += str(self.TheImage[LineNumber][-(8-x)][0] % 2)
        return value

    # Return the ID of the data of this name
    def GetUniqueID(self, Name):
        if self.array.get(Name):
            return self.array[Name]
        else:
            print(f"No Data with this name{Name}")
            return


    # Return the value of the data
    def GetInfo(self, Name):
        UniqueID = self.GetUniqueID(Name)
        if (UniqueID is None):
            return

        img1 = self.ReadCharacterCount(UniqueID)
        CharactersCount = int(self.BinaryToNumber(img1))
        return self.ReadData(UniqueID, CharactersCount)

    # Read the value of the data from the image
    def ReadData(self, Line, NumberOfCharacters):
        row = 0
        value = ""
        while (row != NumberOfCharacters * 8):
            value += str(self.TheImage[row][Line][0] % 2)
            row += 1
            Line += 1
        return self.BinaryToString(value)

    # Set the data value of this data name
    def SetInfo(self, Name,  Value):
        BinaryNumber = self.NumberToBinary(len(str(Value)))
        UniqueID = self.GetUniqueID(Name)
        if (UniqueID is None):
            return
        self.AddCharacterCountToImage(BinaryNumber, UniqueID)
        self.AddBinaryValueToTheImage(self.StringtoBinary(Value), UniqueID)

    # Add the data value as binary to the image in the selected row

    def AddBinaryValueToTheImage(self, BinaryValue, UniqueID):
        index = 0
        for x in range(UniqueID, UniqueID+len(BinaryValue)):
            self.TheImage[index][x] = self.AddBitToPixel(
                self.TheImage[index][x], 0, BinaryValue[index])
            index += 1

    # Convert Number into binary of 8 bits

    def NumberToBinary(self, Num):
        binaryval = bin(Num)[2:]
        while (len(binaryval) < 8):
            binaryval = "0"+binaryval
        return str(binaryval)

    # Convert Binary to number
    def BinaryToNumber(self, Num):
        Number = int(Num)
        Multiplier = 1
        Value = 0
        while Number != 0:
            bit = Number % 10
            Value += int(Multiplier*bit)
            Multiplier *= 2
            Number = int(Number/10)
        return Value

    # Return the pixel after adding the bit to the index(index)of the pixel
    def AddBitToPixel(self, pixel, index, value):
        if pixel[index] % 2 != int(value):
            pixel[index] += 1
        return pixel

    # Get The indicator of the picture (the pixel of last column and last row)
    def Indicator(self, PictureAsArray):
        LastPixel = PictureAsArray[-1][-1]
        return [LastPixel[0] % 2, LastPixel[1] % 2, LastPixel[2] % 2]

    # Convert Series of bits into string (Each character 8 bits )
    def BinaryToString(self, BinaryArray):
        value = ""
        for x in range(0, len(BinaryArray), 8):
            temp = BinaryArray[x:x+8]
            value += chr(self.BinaryToNumber(temp))
        return value

    # Convert string into series of bits (Each character is 8 bits )

    def StringtoBinary(self, string):
        return ''.join('{0:08b}'.format(ord(x), 'b') for x in str(string))

    def GetStudentInformation(self):
        information = {}
        for item in self.array:
            information[item] = self.GetInfo(item)
        return information
##########################################################################################################

#Transcript Methods

    def ReadStudentMarks(self, file):
        transcript = []
        with open(file.filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                transcript.append(row)

        return transcript

    def read_marks_from_file(self,path: str):
        transcript = []
        with open(path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                transcript.append((row[0], row[1], row[2]))
        return transcript


    def TranscriptStore(self, transcript,student_id):
        start = ImageData.get_transcript_location(student_id) #self.GetUniqueID("transcript")
        space = 1500//len(transcript)
        self.AddCharacterCountToImage(self.NumberToBinary(len(transcript)), start)

        for index, place in zip(range(0, len(transcript)), range(start, 1700, space)):
            number_of_courses = len(transcript[index][0])
            if number_of_courses < 10:
                binary_number = self.StringtoBinary("0"+str(number_of_courses)) #number of characters in course name
            else:
                binary_number = self.StringtoBinary(str(number_of_courses)) #number of characters in course name
            course_name = self.StringtoBinary(transcript[index][0]) #the course name that we want to store it in the image
            course_mark = self.StringtoBinary(transcript[index][1]) # the student mark that we want to store it in the image with course name
            if not transcript[index][2]:
                course_hours = self.StringtoBinary("N")
            else:
                course_hours = self.StringtoBinary(transcript[index][2]) # the credit hours of the course

            self.AddBinaryValueToTheImage(binary_number, place - 1)
            self.AddBinaryValueToTheImage(course_name, place)
            self.AddBinaryValueToTheImage(course_mark, place + 1)
            self.AddBinaryValueToTheImage(course_hours, place + 2)

        return

    def AddTranscript(self, file_path, student_id):
        transcript_info = self.ReadStudentMarks(file_path)
        self.TranscriptStore(transcript_info, student_id)
        return


    def TranscriptRead(self,student_id):
        transcript_info = dict()
        start = ImageData.get_transcript_location(student_id) #int(self.GetUniqueID("transcript"))
        number_of_courses = self.BinaryToNumber(self.ReadCharacterCount(start))
        space = 1500//number_of_courses
        end = start +(number_of_courses * space)

        for course in range(start, end, space):
            count = self.ReadCourseNameCharacterCount(course - 1)
            course_name = self.ReadData(course,count)
            course_mark = self.ReadData(course+1, 2)
            course_houre = self.ReadData(course+2, 1)
            if course_mark[1] == '+' or course_mark[1] == '-':
                transcript_info.update({course_name: (course_mark, course_houre)})
            else:
                transcript_info.update({course_name: (course_mark[0], course_houre)})
        gpa = self.GPA_calculator(transcript_info)
        transcript_info.update({"GPA": gpa})
        return transcript_info


    def ReadCourseNameCharacterCount(self,UniqueId):
        number_of_characters = self.ReadData(UniqueId, 2)
        return int(number_of_characters)

    def GPA_calculator(self, transcript):
        grades = {'A': 4.0, 'A-': 3.67, 'B+': 3.33, 'B': 3.0, 'B-': 2.67, 'C+': 2.33, 'C': 2.0, 'C-': 1.67, 'D+': 1.33,
                  'D': 1.0, 'F': 0.35}
        summ = 0
        number_of_hours = 0
        for course in transcript:
            if transcript[course][0] in grades:
                summ += grades[transcript[course][0]] * int(transcript[course][1])
                number_of_hours += int(transcript[course][1])
        gpa = summ / number_of_hours
        return gpa

    def AddBinaryPasswordToTheImage(self, BinaryValue, UniqueID):
        index = 0
        for x in range(UniqueID, UniqueID+len(BinaryValue)):
            self.TheImage[x][index] = self.AddBitToPixel(
                self.TheImage[x][index], 0, BinaryValue[index])
            index += 1

    def SetPassword(self, value, student_id):
        BinaryNumber = self.NumberToBinary(len(str(value)))
        UniqueID = ImageData.get_password_location(student_id)

        self.AddCharacterCountToImage(BinaryNumber, UniqueID)
        self.AddBinaryPasswordToTheImage(self.StringtoBinary(value), UniqueID)

    def ReadPassword(self, student_id):
        UniqueID = ImageData.get_password_location(student_id)
        img1 = self.ReadCharacterCount(UniqueID)
        CharactersCount = int(self.BinaryToNumber(img1))
        row = 0
        value = ""
        while (row != CharactersCount * 8):
            value += str(self.TheImage[UniqueID][row][0] % 2)
            row += 1
            UniqueID += 1
        return self.BinaryToString(value)

