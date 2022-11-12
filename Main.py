import sys
import numpy as np
from PIL import Image


class MyStruct():

    def __init__(self, Header, Value):
        self.Header = Header
        self.Value = Value


class Studentimage():
    array = []

    def __init__(self, ImagePath):
        self.ImagePath = ImagePath
        self.TheImage = np.asarray(Image.open(ImagePath))
        self.array.append(MyStruct("Name", 5))
        self.array.append(MyStruct("Address", 17))
        self.array.append(MyStruct("ID", 23))
        self.array.append(MyStruct("GPA", 106))

    def Save(self):
        img = Image.fromarray(self.TheImage)
        img.save(self.ImagePath)

    def AddBinaryNumberToTheImage(self, BinaryArray, LineNumber):
        index = 0
        for x in range(0, len(BinaryArray)):
            self.TheImage[LineNumber][-(8-x)] = self.AddBitToPixel(self.TheImage[LineNumber]
                                                                   [len(self.TheImage) - len(BinaryArray) + x], index, BinaryArray[x])

    def NumberToBinary(self, Num):
        binaryval = bin(Num)[2:]
        while (len(binaryval) < 8):
            binaryval = "0"+binaryval
        return str(binaryval)

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
        return self.BinaryToNumber(img1)

    def SetInfo(self, Value, Name):
        BinaryNumber = self.NumberToBinary(Value)
        UniqueID = self.GetUniqueID(Name)
        if (UniqueID is None):
            return
        self.AddBinaryNumberToTheImage(BinaryNumber, UniqueID)

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

    def AddBitToPixel(self, pixel, index, value):
        if pixel[index] % 2 != int(value):
            pixel[index] += 1
        return pixel

    def Indicator(PictureAsArray):
        LastPixel = PictureAsArray[-1][-1]
        return [LastPixel[0] % 2, LastPixel[1] % 2, LastPixel[2] % 2]


img = Studentimage("D:/Images/Image11.png")
img.SetInfo(255, "Name")
img.Save()
print(img.GetInfo("GPA"))
