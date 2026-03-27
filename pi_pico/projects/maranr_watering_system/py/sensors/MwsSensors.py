# MwsSensors.py

import asyncio
import gc
import utime as time
import machine

from logger_elem.ElemLoggerABC import ElemLoggerABC
from lib2.DataBoard import DataBoard
from utils import get_fs_space_string
from utils import get_memory_status_string

log = None
logrt = None
logi = None


class MwsSensors(ElemLoggerABC):
    """ sensors and effectors """

    def __init__(self, *args):
        self._data_board = None
        super().__init__()


    def _set_logger(self, logger):
        global log, logrt, logi
        log = logger.log
        logrt = logger.logrt
        logi = logger.logi


    def start_the_task(self):
        """ creates,starts the coro. Returns task."""
        logi("MwsSensors.start_the_task  STARTING THE SENSOR TASK!")

        self._data_board = DataBoard.get_instance()

        task = asyncio.create_task(self.sensors_coro())
        return task


    async def sensors_coro(self):

        log_limit_ctr = 0
        while 1:
            if 0:
                fss = get_fs_space_string()
                log(f"SENSORS@48.sensors_coro RUNNING: {fss}")
            if 0:
                mss = get_memory_status_string(do_garbage_collect=False)
                log(f"SENSORS@51.sensors_coro MEMORY before GC: {mss} ++++++++++++++++++++++++++++++++++++")
                gc.collect()
                mss = get_memory_status_string(do_garbage_collect=False)
                log(f"SENSORS@54.sensors_coro MEMORY after  GC: {mss} ++++++++++++++++++++++++++++++++++++")

            # Reduce logging volume/freq
            log_limit_ctr += 1
            if log_limit_ctr >= 6:
                log_limit_ctr = 0
                use_logi = True
            else:
                use_logi = False

            if 1:
                ma_before = gc.mem_alloc()
                mf_before = gc.mem_free()
                gc.collect()
                ma_after = gc.mem_alloc()
                mf_after = gc.mem_free()
                ma_diff = ma_after - ma_before
                mf_diff = mf_after - mf_before
                m1 = f"SENSORS@63  ++++++++++  Alloc:  {ma_after} - {ma_before}  ==>  DIFF: {ma_diff} +++++++++++++++++++++++++++++++++++++++"
                m2 = f"SENSORS@64  ++++++++++  Free:   {mf_after} - {mf_before}  ==>  DIFF: {mf_diff}  +++++++++++++++++++++++++++++++++++++++"
                if use_logi:
                    logi(m1); logi(m2)
                else:
                    log(m1); log(m2)

            self._get_internal_temps(use_logi)

            await asyncio.sleep(10)


    def _get_internal_temps(self, use_logi):
        temperature_c = read_internal_temperature()
        temperature_f = celsius_to_fahrenheit(temperature_c)
        self._data_board.set_internal_temps(temperature_f, temperature_c);

        m = f"SENSORS@74  Internal Temperature: {temperature_c:10.4f} °C   {temperature_f:10.4f} °F"
        if use_logi:
            logi(m)
        else:
            log(m)


adcpin = 4
sensor = machine.ADC(adcpin)

def read_internal_temperature():
    adc_value = sensor.read_u16()
    voltage = (3.3 / 65535) * adc_value
    temperature_celsius = 27 - (voltage - 0.706) / 0.001721
    return temperature_celsius

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32



#    def make_space_stg(self):
#        ts, fs = get_flash_space()
#
#        tss = convert_fs_space_to_string(ts)
#        fss = convert_fs_space_to_string(fs)
#
#        s = f"TOTAL SPACE {tss}   FREE SPACE {fss}"
#        return s
#
###

