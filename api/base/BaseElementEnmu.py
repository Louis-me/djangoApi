import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Element(object):
    REPORT_FILE = PATH("../Report/") # 测试报告
    PICT_PARAM = PATH("../Log/param.txt") # 写入pict需要的参数
    PICT_PARAM_RESULT = PATH("../Log/param_result.txt") # pict生成后的数据

    ERROR_EMPTY = "error_empty"
    ERROR_VALUE = "error_value"
    RIGHT_VALUE = "right_value"
    C_CHECK = {"passed": 0, "failed": -1, "no_check": -2}
