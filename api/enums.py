from enum import Enum


class Cities(Enum):
    # ISO_3166-2:TW
    TPE = "Taipei"
    NWT = "NewTaipei"
    TAO = "Taoyuan"
    TXG = "Taichung"
    TNN = "Tainan"
    KHH = "Kaohsiung"
    KEE = "Keelung"
    HSZ = "Hsinchu"
    HSQ = "HsinchuCounty"
    MIA = "MiaoliCounty"
    CHA = "ChanghuaCounty"
    NAN = "NantouCounty"
    YUN = "YunlinCounty"
    CYQ = "ChiayiCounty"
    PIF = "PingtungCounty"
    ILA = "YilanCounty"
    HUA = "HualienCounty"
    TTT = "TaitungCounty"
    KIN = "KinmenCounty"
    PEN = "PenghuCounty"
    LIE = "LienchiangCounty"


class Directions(Enum):
    """去返程 [0:'去程',1:'返程',2:'迴圈',255:'未知']"""
    GO = 0
    BACK = 1
    LOOP = 2

    UNKNOWN = 255


class A2EventTypes(Enum):
    """進站離站 : [0:'離站',1:'進站']"""
    EXIT = 0
    ENTER = 1
