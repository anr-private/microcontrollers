# ElemLogger.py
#
# Elementary logger

PRT=True
def prt(s):
    if PRT: print (s)


class ElemLogger:

    def __init__(self, simplified_class_name):
        self.class_name = simplified_class_name
        prt(f"ElemLogger@14 init {self.class_name=}")



    def log(self, mesg):
        print(f"ElemLogger@19.log '{mesg=}' ")

    def logrt(self, mesg):
        print(f"ElemLogger@22.logrt '{mesg=}' ")

    def logi(self, mesg):
        print(f"ElemLogger@25.logi '{mesg=}' ")



    def __str__(self):
        s = []
        s.append("cls=%s" % str(self.class_name))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))




###
