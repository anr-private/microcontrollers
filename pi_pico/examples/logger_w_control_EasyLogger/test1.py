# test

from logger.EasyLogger import EasyLogger

class ClassA:
    
    def __init__(self, rrr):
        self.rrr = rrr

class ClassB:
    
    def __init__(self, rrr):
        self.rrr = rrr


if 0:
    aa = ClassA(EasyLogger.log_log_)
    bb = ClassB(EasyLogger.log_log_)

el = EasyLogger.get_instance()

#aa = ClassA(el.log_log_)
#bb = ClassB(el.log_log_)
aa = ClassA(el.log_mute_)
bb = ClassB(el.log_mute_)

print(f"aa {aa.rrr}")
print(f"bb {bb.rrr}")

if 0:
    jj = EasyLogger.get_instance()
    print(f"is el jj   {el is jj}")

print(f" IS?  {aa.rrr is bb.rrr}")

print(f" IS STG same?  {str(aa.rrr) == str(bb.rrr)}")
print(f"  stg is {str(aa.rrr)}")


#print(f"  {dir(aa.rrr)}")
#print(f"  {dir(bb.rrr)}")


###
