# Trivlog.py


VALIDATE = 13524690

PRT=True
def prt(s):
    if PRT: print (s)


class Trivlog:

    _instance = None

    # unit test 
    _latest_log_mesg = None
    _latest_logrt_mesg = None
    _latest_logi_mesg = None
    _latest_log_mute_mesg = None

    _show_log_muted_mesg = True

    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = Trivlog(VALIDATE)
        return cls._instance


    def __init__(self, validate=None):
        if validate != VALIDATE:
            m = f"Trivlog@10.init DISALLWED: CALLING Trivlog CTOR"
            raise RuntimeError(m)

        # key:   str   "<class 'test_classes.ClassA.ClassA'>"  NOTE embedded quotes
        # value: list of  class-objects  [ <class 'test_classes.ClassA.ClassA'>, ... ]
        #@@@@@@@@@@@@@@


        # key:   class-object   <class 'test_classes.ClassA.ClassA'>
        # value: list of instances  [ <obj-of-class-A>, ... ]
        self._classes_to_instances = {}

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        Trivlog._instance = None
        Trivlog._clear_latest_messages()

    @classmethod
    def _clear_latest_messages(cls):
        # UNIT TEST ONLY
        Trivlog._latest_log_mesg = None
        Trivlog._latest_logrt_mesg = None
        Trivlog._latest_logi_mesg = None
        Trivlog._latest_log_mute_mesg = None


    def register_user_class(self, obj_instance):
        # obj is a user obj that subclasses TrivlogABC
        # Returns a tuple of the log functions the caller should use
        global _show_log_muted_mesg #@@@@@@@@@@@@@@@@@@@@@@@@

        prt(f"Trivlog@61   {repr(obj_instance)=}")
        try:
            prt(f"Trivlog@63   {str(obj_instance)=}")
        except  Exception as ex:
            pass
            # exception if ctor has not finished yet.
            ###prt(f"Trivlog@65 register_user_class  str(obj_instance) FAILED. Probably still in ctor.  ex={repr(ex)}  ex={str(ex)} ")
    
        # get the Class of the obj_instance
        cls_obj = type(obj_instance)
        prt(f"Trivlog@31  register {cls_obj=}  type={type(cls_obj)}")        
        #cls_stg = str(cls_obj)
        #prt(f"Trivlog@33 @@@@@@@@@@@@@@@@ register {cls_stg=}")        

        instances_of_cls = self._classes_to_instances.get(cls_obj)
        if not instances_of_cls:
            instances_of_cls = [obj_instance]
            self._classes_to_instances[cls_obj] = instances_of_cls
        else:
            instances_of_cls.append(obj_instance)
        if 0:
            # THIS FIXES THE MEMORY LEAK - objects were being GC'd but
            # not removed from the _classes_to_instances dict.
            # Need to use weak refs to the objects.
            # But trying a new approach: logger_elem.
            prt(f"Trivlog@62  number of registered classes:  {len(self._classes_to_instances)}")
            print("TRIVLOG 85  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"*2)
            print("TRIVLOG 85  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"*2)
            print(f" ... clearing ithe instances dict   size is {len(self._classes_to_instances)} ")
            self._classes_to_instances = {}
            print("TRIVLOG 85  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"*2)
            print("TRIVLOG 85  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"*2)
            print("TRIVLOG 85  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"*2)
        
        if self._show_log_muted_mesg:
            _show_log_muted_mesg = False
            print("@@@@@@@@@@@@@@ Trivlog@82  LOG IS MUTED !!!!!!!!!!!!!!!!!!!!!!!!!!-----------------------------------")
            print("@@@@@@@@@@@@@@ Trivlog@82  LOG IS MUTED !!!!!!!!!!!!!!!!!!!!!!!!!!-----------------------------------")
            print("@@@@@@@@@@@@@@ Trivlog@82  LOG IS MUTED !!!!!!!!!!!!!!!!!!!!!!!!!!-----------------------------------")
        ### TEMP TURNED OFF: MUTE the log() function 
        ###    return self._log, self._logrt, self._logi
        return self._log_mute, self._logrt, self._logi


    # === METHODS for Querying and Controlling the logging in registered classes
    #             IE for use by GUI/webpage/etc

    def get_registered_classes(self):
        # returns a copy of the dict of registered classes
        prt(f"Trivlog@70.get_registered_classes  {self.classes=}")
        #@@@return {item[0]:item[1] for item in self.classes.items()}

    def get_number_of_registered_classes(self):
        return len(self._classes_to_instances)

    def get_class_obj(self, full_class_name):
        pass# returns Class obj 
        #@@@return self.classes.get(full_class_name)

    def set_logging_enabled_in_all_classes(self, enable):
        if enable:
            log_f   = self._log
            logrt_f = self._logrt
            logi_f  = self._logi
        else:
            log_f   = self._log_mute
            logrt_f = self._logrt  # DO NOT DISABLE
            logi_f  = self._logi   # DO NOT DISABLE

        # set/reset logging in all registered classes
        ctr = 0
        for cls,instances in self._classes_to_instances.items():
            prt(f"Trivlog@83.set_logging_enabled_in_all_classes class={cls}")
            prt(f"Trivlog@83.set_logging_enabled_in_all_classes instances={instances}")
            for inst in instances:
                prt(f"Trivlog@86.set_logging_enabled_in_all_classes {enable=} {inst=}")
                inst._set_log_functions(log_f, logrt_f, logi_f)
                ctr += 1
        prt("Trivlog@99 set_logging_enabled_in_all_classes {enable=} Objects updated {ctr}")

    # === LOGGING METHODS for use by 'user' classes ==================

    def _log(self, mesg):
        ###prt(f"Trivlog._log mesg='{mesg}'")
        prt(mesg)
        Trivlog._latest_log_mesg = mesg


    def _logrt(self, mesg):
        prt(f"Trivlog._logrt mesg='{mesg}'")
        Trivlog._latest_logrt_mesg = mesg

    def _logi(self, mesg):
        prt(f"Trivlog._logi mesg='{mesg}'")
        Trivlog._latest_logi_mesg = mesg

    def _log_mute(self, mesg):
        #@@@@@@@@@@@@@@@@@@@@@@@@@prt(f"Trivlog._log_mute _MUTED_ mesg='{mesg}'")
        Trivlog._latest_log_mute_mesg = mesg


    def __str__(self):
        s = []
        s.append("num.registered=%s" % len(self._classes_to_instances))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))

    @classmethod
    def _get_prt_status(self):
        # unit test
        global PRT 
        return PRT

    @classmethod
    def _enable_prt(self, enabled=True):
        # unit test
        global PRT 
        PRT = not not enabled

###
