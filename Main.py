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

    def ToPicture(self):
        img = Image.fromarray(self.TheImage)
        img.save(self.ImagePath)

    def AddBinaryNumberToTheImage(self, BinaryArray, LineNumber):
        index = 0
        for x in range(0, len(BinaryArray)):
            self.TheImage[LineNumber][-(8-x)] = AddBitToPixel(self.TheImage[LineNumber]
                                                              [len(self.TheImage) - len(BinaryArray) + x], index, BinaryArray[x])

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
        img1 = self.ReadFromArray(UniqueID)
        return (img1)


def NumberToPinary(Num):
    binaryval = bin(Num)[2:]
    return binaryval


def BinaryToNumber(Num):
    Number = int(Num)
    Multiplier = 1
    Value = 0
    while Number != 0:
        bit = Number % 10
        Value += int(Multiplier*bit)
        Multiplier *= 2
        Number = int(Number/10)
    return Value


def AddBitToPixel(pixel, index, value):
    if pixel[index] % 2 != int(value):
        pixel[index] += 1
    return pixel


def ReturnIndicatorPixelAsArray(PictureAsArray):
    LastPixel = PictureAsArray[-1][-1]
    return [LastPixel[0] % 2, LastPixel[1] % 2, LastPixel[2] % 2]


# def SetInfo(img, Value, Name):
#     UniqueID = GetUniqueID(Name)
#     img1 = AddBinaryNumberToArray(img, Value, UniqueID)
#     return img1


img = Studentimage("D:/Images/Image11.png")
img.AddBinaryNumberToTheImage("00110011", 1079)
print(img.GetInfo("Address"))
