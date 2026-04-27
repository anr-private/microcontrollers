# DataBoard.py
#
# Global data board
#
# Running average:   Average =+ (next_value - Average) / new-sample-count

from logger_elem.ElemLoggerABC import ElemLoggerABC


# Logging functions; provided by our parent class using set_log_functions()
log = None
logrt = None
logi = None

VALIDATE = 192756


class DataBoard(ElemLoggerABC):

    SYS_STATE_STARTUP = 0
    SYS_STATE_OFF     = 1
    SYS_STATE_OFF     = 2
    SYS_STATE_OFF     = 3
    SYS_STATE_OFF     = 4


    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is not None: return cls._instance
        cls._instance = DataBoard(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls):
        # UNIT TEST ONLY
        DataBoard._instance = None
        ###DataBoard._clear_latest_messages()


    def __init__(self, validate):
        if validate != VALIDATE:
            raise RuntimeError(f"DataBoard CTOR is private!")
        self.system_state = self.SYS_STATE_STARTUP
        self.ipaddr = None
        self.port = 0
        self.webserver_active = False
        self.internal_temp_f = 0
        self.internal_temp_c = 0
        self.time_mgr_latest_ntp_update_secs = 0
        self.time_mgr_number_of_ntp_updates = 0
        self.time_mgr_number_of_time_jumps = 0
        self.time_mgr_maximum_time_jump_secs = 0
        super().__init__()

    def _set_logger(self, logger):
        global log, logrt, logi
        #print(f"DataBoard@59 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def set_ip_and_port(self, ipaddr, port):
        self.ipaddr = ipaddr
        self.port = port
        print(f"DataBoard@68  SET IPADDR={self.ipaddr}  PORT={self.port} ")


    def post_time_mgr_status(self, 
                        latest_ntp_update_secs,
                        number_of_ntp_updates,
                        number_of_time_jumps,
                        maximum_time_jump_secs):

        self.time_mgr_latest_ntp_update_secs = latest_ntp_update_secs
        self.time_mgr_number_of_ntp_updates = number_of_ntp_updates
        self.time_mgr_number_of_time_jumps = number_of_time_jumps
        self.time_mgr_maximum_time_jump_secs = maximum_time_jump_secs


    def set_internal_temps(self, degsF, degsC):
        self.internal_temp_f = degsF
        self.internal_temp_c = degsC

    def get_internal_temps_one_dec_place(self):
        degs_f = f"{self.internal_temp_f:.1f}"
        degs_c = f"{self.internal_temp_c:.1f}"
        return degs_f, degs_c


    def __str__(self):
        s = []
        s.append("x=%s" % str(self.x))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))

    def status_lines(self):
        lines = []
        lines.append(f"DataBoard State:  {self.system_state}")
        lines.append(f" NTP Latest update: {self.time_mgr_latest_ntp_update_secs}  number-of-NTP-updates {self.time_mgr_number_of_ntp_updates}")
        lines.append(f" NTP Number-of-time-jumps: {self.time_mgr_number_of_time_jumps}  Max.time-jump-secs: {self.time_mgr_maximum_time_jump_secs}  ")
        lines.append(f" IP:port {self.ipaddr}:{self.port}   Webserver:{'Active' if self.webserver_active else 'Inactive'}")
        lines.append(f" system.state={self.system_state} ")
        lines.append(f" Internal temp: {self.internal_temp_f} F  {self.internal_temp_c} C")
        return lines

    def long_string(self):
        return "\n".join(self.status_lines())


###
