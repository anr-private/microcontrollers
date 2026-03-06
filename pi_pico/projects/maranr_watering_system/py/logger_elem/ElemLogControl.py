# ElemLogControl.py
# 
# Control and registrar for ElemLogger

from .ElemLogger import ElemLogger

VALIDATE = 13524690

PRT=True
def prt(s):
    if PRT: print (s)


class ElemLogControl:

    _instance = None

    # key: simplified class name   value: ElemLogger for that class
    registry = {}

    
    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = ElemLogControl(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        ElemLogControl._instance = None
        ElemLogControl._clear_latest_messages()


    def __init__(self, validate=None):
        if validate != VALIDATE:
            m = f"ElemLogControl@34 CALLED CTOR use get_instance()"
            raise RuntimeError(m)


    def register_user_class(self, obj_instance):
        # obj is a user obj that subclasses ElemLogControlABC
        # Returns a tuple of the log functions the caller should use

        prt(f"ElemLogControl@42   obj is {repr(obj_instance)} ")

        # get the Class of the obj_instance
        #cls_obj = type(obj_instance)
        #prt(f"ElemLogControl@46  register obj={repr(cls_obj)}  type={type(cls_obj)}")        
        #cls_stg = str(cls_obj)
        #prt(f"ElemLogControl@33 @@@@@@@@@@@@@@@@ register {cls_stg=}")        

        simplified_class_name = extract_simplified_classname(obj_instance)
        prt(f"ElemLogControl@51 {simplified_class_name=}")

        # does this class have a logger assigned?
        logger = self.registry.get(simplified_class_name)
        prt(f"ElemLogControl@55  logger of {simplified_class_name} is {logger}")
        if logger is None:
            logger = ElemLogger(simplified_class_name)
            self.registry[simplified_class_name] = logger
        return logger


    def junkkk(self, obj_instance):#@@@@@@@@@@@@@@@@@@
        instances_of_cls = self._classes_to_instances.get(cls_obj)
        if not instances_of_cls:
            instances_of_cls = [obj_instance]
            self._classes_to_instances[cls_obj] = instances_of_cls
        else:
            instances_of_cls.append(obj_instance)
        prt(f"ElemLogControl@62  number of registered classes:  {len(self._classes_to_instances)}")
        return self._log, self._logrt, self._logi




def extract_simplified_classname(obj_instance):
    # given a full class name string like "abc.def.MyClass"; return "MyClass"
    # Obtain the string using  str(obj.__class__)
    obj_repr = repr(obj_instance)
    prt(f"ElemLogControl@70 extract_simplified_classname   {obj_repr=}")
    parts = obj_repr.rsplit(".", 1)
    prt(f"ElemLogControl@73  {parts=}")
    name_and_addr = parts[-1]
    parts = name_and_addr.split(None, 1)
    prt(f"ElemLogControl@76  {parts=}")

    simplified_class_name = parts[0]
    return simplified_class_name

###
