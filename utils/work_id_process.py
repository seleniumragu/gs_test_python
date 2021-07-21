import os

work_id = 0


class ProcessManage(object):

    def __init__(self,parallel_flag,process_name):

        global work_id
        if parallel_flag.lower() == 'true':
            workid = process_name
            if workid == "gw0":
                work_id = 1
            elif workid == "gw1":
                work_id = 2
            else:
                raise Exception("Currently framework is design to support 2 mobile device parallel execution,"
                                "can not support more than 2 mobile devices")

    @classmethod
    def setupworkprocess(cls,parallel_flag,process_name):
        cls(parallel_flag = parallel_flag,process_name = process_name)


def get_work_id():
    return work_id