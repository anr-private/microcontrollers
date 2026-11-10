# DataBoard.py
#
# Global data board
#
# Running average:   Average =+ (next_value - Average) / new-sample-count
# LINEMARKER=DBRD

from logger_elem.ElemLoggerABC import ElemLoggerABC

try: from typing import Callable, Any
except ImportError: pass

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

    _instance: "DataBoard | None" = None

    @classmethod
    def get_instance(cls) -> "DataBoard":
        if cls._instance is not None: return cls._instance
        cls._instance = DataBoard(VALIDATE)
        return cls._instance

    @classmethod
    def _nullify_instance(cls) -> None:
        # UNIT TEST ONLY
        DataBoard._instance = None
        ###DataBoard._clear_latest_messages()


    def __init__(self, validate:int) -> None:
        if validate != VALIDATE:
            raise RuntimeError(f"DataBoard CTOR is private!")
        # All classes use these to access the various classes.
        # This ensures the order of creation does not cause 
        # problems. The classes are first created in
        # maranr_watering_system_main.py:main()
        self.time_mgr: Any = None  # TimeMgr
        self.displays: Any = None    # MwsDisplays
        self.buttons: Any = None     # MwsButtons
        self.sensors: Any = None     # MwsSensors
        self.wifi: Any = None        # MwsWifi
        # 
        self.system_state: int = self.SYS_STATE_STARTUP
        self.ipaddr: str = ""
        self.port: int = 0
        self.webserver_active: bool = False
        self.wifi_restarts_counter: int = 0
        # CPU/Pico board temp
        self.internal_temp_f: int = 0
        self.internal_min_temp_f: int = 9999
        self.internal_max_temp_f: int = 0
        self.internal_temp_c: int = 0
        self.internal_min_temp_c: int = 9999
        self.internal_max_temp_c: int = 0
        #
        self.time_mgr_latest_ntp_update_secs: int = 0
        self.time_mgr_number_of_ntp_updates: int = 0
        self.time_mgr_number_of_time_jumps: int = 0
        self.time_mgr_maximum_time_jump_secs: int = 0
        #
        self.memory_alloc: int = 0
        self.memory_alloc_min: int = 9999999
        self.memory_alloc_max: int = 0
        self.memory_free: int = 0
        self.memory_free_min: int = 9999999
        self.memory_free_max: int = 0

        super().__init__()

    def _set_logger(self, logger: Any) -> None:
        global log, logrt, logi
        #print(f"DBRD$86 _set_logger: {repr(logger)}")
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def set_ip_and_port(self, ipaddr: str, port:int) -> None:
        self.ipaddr = ipaddr
        self.port = port
        print(f"DBRD$95  SET IPADDR={self.ipaddr}  PORT={self.port} ")

    def set_wifi_restarts_counter(self, new_restarts_counter: int) -> None:
        self.wifi_restarts_counter = new_restarts_counter
        print(f"DataBoard.set_wifi_restarts_counter  ctr={self.wifi_restarts_counter}")


    def post_time_mgr_status(self, 
                        latest_ntp_update_secs: int,
                        number_of_ntp_updates: int,
                        number_of_time_jumps: int,
                        maximum_time_jump_secs: int) -> None:

        self.time_mgr_latest_ntp_update_secs = latest_ntp_update_secs
        self.time_mgr_number_of_ntp_updates = number_of_ntp_updates
        self.time_mgr_number_of_time_jumps = number_of_time_jumps
        self.time_mgr_maximum_time_jump_secs = maximum_time_jump_secs


    def set_internal_temps(self, degs_f: int, degs_c: int) -> None:
        self.internal_temp_f = degs_f
        self.internal_min_temp_f = min(self.internal_min_temp_f, degs_f)
        self.internal_max_temp_f = max(self.internal_max_temp_f, degs_f)
        #
        self.internal_temp_c = degs_c
        self.internal_min_temp_c = min(self.internal_min_temp_c, degs_c)
        self.internal_max_temp_c = max(self.internal_max_temp_c, degs_c)

    def get_internal_temps_one_dec_place(self) -> tuple[str,str]:
        degs_f = f"{self.internal_temp_f:.1f}"
        degs_c = f"{self.internal_temp_c:.1f}"
        return degs_f, degs_c

    def get_internal_min_temps_one_dec_place(self) -> tuple[str,str]:
        degs_f = f"{self.internal_min_temp_f:.1f}"
        degs_c = f"{self.internal_min_temp_c:.1f}"
        return degs_f, degs_c

    def get_internal_max_temps_one_dec_place(self) -> tuple[str,str]:
        degs_f = f"{self.internal_max_temp_f:.1f}"
        degs_c = f"{self.internal_max_temp_c:.1f}"
        return degs_f, degs_c


    def set_memory_alloc_and_free(self, mem_alloc: int, mem_free: int) -> None:
        self.memory_alloc = mem_alloc
        self.memory_alloc_min = min(self.memory_alloc_min, mem_alloc)
        self.memory_alloc_max = max(self.memory_alloc_max, mem_alloc)
        self.memory_free = mem_free
        self.memory_free_min = min(self.memory_free_min, mem_free)
        self.memory_free_max = max(self.memory_free_max, mem_free)

    def get_loggable_lines(self, prefix:str="", suffix:str="") -> list[str]:
        # for logging, prefix is usu 'RHDATA$148', suffix is '<br>\n'
        lines = []
        lines.append(f"{prefix}DataBoard State:  {self.system_state} {suffix}")
        lines.append(f"{prefix} NTP Latest update: {self.time_mgr_latest_ntp_update_secs}  number-of-NTP-updates {self.time_mgr_number_of_ntp_updates} {suffix}")
        lines.append(f"{prefix} NTP Number-of-time-jumps: {self.time_mgr_number_of_time_jumps}  Max.time-jump-secs: {self.time_mgr_maximum_time_jump_secs}   {suffix}")
        lines.append(f"{prefix} IP:port {self.ipaddr}:{self.port}   Webserver:{'Active' if self.webserver_active else 'Inactive'} {suffix}")
        lines.append(f"{prefix} Wifi restartsCtr: {self.wifi_restarts_counter} {suffix}")
        lines.append(f"{prefix} system.state={self.system_state}  {suffix}")
        lines.append(f"{prefix} Internal temp: {self.internal_temp_f} F  {self.internal_temp_c} C {suffix}")
        return lines

    def __str__(self) -> str:
        s = []
        s.append("system_state=%s" % str(self.system_state))
        return ("%s[%s]" % 
            (self.__class__.__name__, ",".join(s)))


###
