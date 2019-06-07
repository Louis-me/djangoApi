# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from .BaseOperate import OperateElement
import time
from .BaseElementEnmu import Element as be
import os
from .BaseError import get_error

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class PagesObjects:
    '''
    page层
    kwargs: WebDriver driver, String path(yaml配置参数)
    isOperate: 操作失败，检查点就失败
    test_case：
    test_step：
    '''

    def __init__(self, kwargs):
        self.driver = kwargs["driver"]

        if kwargs.get("home_url", "0") != "0":  # 若为空， 刷新页面
            self.driver.get(kwargs["home_url"])
            print("====home_url=%s===========" % kwargs["home_url"])
        self.operateElement = ""
        self.isOperate = True
        self.name = kwargs["name"]
        self.test_step = kwargs["test_step"]
        self.test_check = kwargs.get("test_check", "0")
        self.log_test = kwargs["log_test"]

    '''
     操作步骤
    '''

    def operate(self):
        self.operateElement = OperateElement(self.driver)
        for item in self.test_step:
            result = self.operateElement.operate(item, self.name, self.log_test)
            if not result["result"]:
                msg = get_error({"type": be.DEFAULT_ERROR, "element_info": item["element_info"]})
                self.log_test.build_start_line(msg)
                self.isOperate = False
                return False
            if item.get("is_time", "0") != "0":
                time.sleep(item["is_time"])  # 等待时间
        return True

    def check_point(self):
        return self.__check()

    '''
    检查点
    log_test： 日志记录
    '''

    def __check(self):
        if len(self.test_check) == 0:
            return be.C_CHECK["failed"]
        if self.isOperate:
            for item in self.test_check:
                resp = self.operateElement.operate(item, self.name, self.log_test)
                # 默认检查点，就是查找页面元素
                if not resp["result"]:
                    m = get_error({"type": be.DEFAULT_CHECK, "element_info": item["element_info"], "info": item["name"]})
                    print("__check=%s" % m)
                    self.log_test.build_start_line(m)
                    return be.C_CHECK["failed"]
        else:
            return be.C_CHECK["failed"]
        return be.C_CHECK["passed"]
