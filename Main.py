import sys
import numpy as np
from PIL import Image


class ImageData():

    def __init__(self, Header, Value):
        self.Header = Header
        self.Value = Value


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


class Studentimage():

    def __init__(self, ImagePath):
        self.ImagePath = ImagePath
        self.TheImage = np.asarray(Image.open(ImagePath))
        self.array = array
    # Save the changes of the image after editing.

    def Save(self):
        img = Image.fromarray(self.TheImage)
        img.save(self.ImagePath)

    # Add The count of the characters to the image as binary
    def AddCharacterCountToImage(self, BinaryArray, LineNumber):
        index = 0
        for x in range(0, len(BinaryArray)):
            self.TheImage[LineNumber][-(8-x)] = self.AddBitToPixel(self.TheImage[LineNumber]

                                                                   [len(self.TheImage) - len(BinaryArray) + x], index, BinaryArray[x])

    #

    def ReadFromArray(self, LineNumber):
        value = ""
        for x in range(0, 8):
            value += str(self.TheImage[LineNumber][-(8-x)][0] % 2)
        return value

    def GetUniqueID(self, Name):
        myitem = {}
        for item in self.array:
            if (item.Header == Name):
                myitem = item
        if (myitem == {}):
            print("No Data with this name")
            return
        return myitem.Value

    def GetInfo(self, Name):
        UniqueID = self.GetUniqueID(Name)
        if (UniqueID is None):
            return

        img1 = self.ReadFromArray(UniqueID)
        CharactersCount = int(self.BinaryToNumber(img1))
        self.ReadData(UniqueID, CharactersCount)

    def ReadData(self, Line, NumberOfCharacters):
        row = 0
        value = ""
        while (row != NumberOfCharacters * 8):
            value += str(self.TheImage[row][Line][0] % 2)
            row += 1
            Line += 1
        print(self.BinaryToString(value))

    def SetInfo(self, Name,  Value):
        BinaryNumber = self.NumberToBinary(len(Value))
        UniqueID = self.GetUniqueID(Name)
        if (UniqueID is None):
            return
        self.AddCharacterCountToImage(BinaryNumber, UniqueID)
        self.AddBinaryValueToTheImage(self.StringtoBinary(Value), UniqueID)

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
    def BinaryToString(self, BinaryArray,):
        value = ""
        for x in range(0, len(BinaryArray), 8):
            temp = BinaryArray[x:x+8]
            value += chr(self.BinaryToNumber(temp))
        return value

    # Convert string into series of bits (Each character is 8 bits )

    def StringtoBinary(self, string):
        return (''.join('{0:08b}'.format(ord(x), 'b') for x in string))

# The types of data we can edit in the picture :
# Note: U need to set the data at least once for each picture.
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
img = Studentimage("D:/Images/Image11.png")

# Both arguments should be strings.
img.SetInfo("GPA", "3.5")

# Image need to be saved after finishing editing.
img.Save()
img.GetInfo("GPA")
