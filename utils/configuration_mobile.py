# -*- coding: utf-8 -*-
from utils.work_id_process import get_work_id

parallelflag=''
platform=''
devicename=''


class ConfigurationSet(object):

    def __init__( self,parallelflag_p,platform_p,devicename_p):


        global parallelflag
        if ("true" in parallelflag_p) or ("false" in parallelflag_p):
            parallelflag = parallelflag_p
        else:
            raise Exception("Parameter 'parallel flag' must be provided, value should be true or false")

        global platform
        if ("ios" in platform_p) or ("android" in platform_p):
            platform = platform_p
        elif "mix" in platform_p :
            if get_work_id() == 1:
                platform = "android"
            elif get_work_id() == 2:
                platform = "ios"
            else:
                raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                                "can not support more than 2 mobile devices")
        else:
            raise Exception("Parameter 'execution platform' value must be provided, "
                            "value should be ios or android or mix for appium execution")

        global devicename
        if ("deviceone" in devicename_p) or ("device1" in devicename_p):
            devicename = devicename_p
        elif ("devicetwo" in devicename_p) or ("device2" in devicename_p):
            devicename = devicename_p
        else:
            raise Exception("device name must be provided, value should be deviceone or devicetwo")


    @classmethod
    def initiateconfigvalue(cls,parallel_flag,plat_form,device_name):
        cls(parallel_flag,plat_form,device_name)


def get_parallel_flag():
    return parallelflag


def get_platform():
    return platform


def get_device_name():
    return devicename
