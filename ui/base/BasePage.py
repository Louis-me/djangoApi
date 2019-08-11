# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from .BaseOperate import OperateElement
import time
from .BaseElementEnmu import Element as be, Element
import os
from .BaseError import get_error
from ..models import  CommonCase
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
        self.step_msg = "" # 操作步骤
        self.check_msg = "" # 检查步骤
        self.extend = "" # 失败原因
    '''
     操作步骤
    '''

    def operate(self):
        self.operateElement = OperateElement(self.driver)
        # ===========把用例步骤和关联的公共用例，重新处理，按照sort来排序 Start======
        data = []
        if len(self.test_step) > 1:
            for item in range(len(self.test_step)):
                for i in self.test_step[item]:
                    data.append(i)
            data_sort = sorted(data, key=lambda e: e.__getitem__('sort'))
        else:
            data_sort = sorted(self.test_step[0], key=lambda e: e.__getitem__('sort'))

        # ==================排序结束 End=========================

    # ========开始执行用例步骤==============
        for j in data_sort:
            if j.get("cc_id", "-1") != "-1": # 如果存在cc_id，表示传过来的是公共用例的列表，需要读取公共用例步骤
                common_case_step = list(CommonCase.objects.get(pk=j["cc_id"]).commoncasestep_set.order_by("sort").values())
                for i in common_case_step:
                    result = self.operateElement.operate(i, self.name, self.log_test)
                    self.step_msg = self.step_msg + self.__operate_type(i) + "\n"
                    if not result["result"]:
                        msg = get_error({"type": be.DEFAULT_ERROR, "element_info": i["element_info"]})
                        print(msg)
                        self.extend = msg
                        self.log_test.build_start_line(msg)
                        self.isOperate = False
                        return False
            else:
                # print("=======正常情况=%s=======" % j)
                result = self.operateElement.operate(j, self.name, self.log_test)
                self.step_msg = self.step_msg + self.__operate_type(j) + "\n"
                if not result["result"]:
                    msg = get_error({"type": be.DEFAULT_ERROR, "element_info": j["element_info"]})
                    print(msg)
                    self.extend = msg
                    self.log_test.build_start_line(msg)
                    self.isOperate = False
                    return False

        return True

    # 0检查是否通过，1为操作步骤，2为检查点步骤,3为失败原因
    def check_point(self):
        return self.__check(), self.step_msg, self.check_msg, self.extend

    '''
    检查点
    log_test： 日志记录
    '''

    def __check(self):
        # 拼接检查点步骤msg
        for tc in self.test_check:
            self.check_msg = self.check_msg + self.__operate_type(tc) + "\n"

        if len(self.test_check) == 0:
            return be.C_CHECK["failed"]
        if self.isOperate:
            for item in self.test_check:
                resp = self.operateElement.operate(item, self.name, self.log_test)
                # 默认检查点，就是查找页面元素
                if not resp["result"]:
                    m = get_error(
                        {"type": be.DEFAULT_CHECK, "element_info": item["element_info"], "info": item["name"]})
                    self.extend = m
                    self.log_test.build_start_line(m)
                    return be.C_CHECK["failed"]
        else:
            return be.C_CHECK["failed"]
        return be.C_CHECK["passed"]

    def __operate_type(self,kw):
        elements = {
            Element.CLICK: lambda: "%s_查找类型为_%s_查找元素为_%s_操作类型为_%s" % (kw["name"], kw["find_type"], kw["element_info"],"点击"),
            Element.SEND_KEYS: lambda: "%s_查找类型为_%s_查找元素为_%s_操作类型为_%s_输入%s" % (kw["name"],kw["find_type"], kw["element_info"],"输入", kw["extend"]),
            Element.SWITCH_TO_WINDOW: lambda: "%s_查找类型为_%s_查找元素为_%s_操作类型为_%s_窗口参数%s" % (kw["name"],"无", "无","切换窗口", kw["extend"]),
            Element.MOVE_TO_ELEMENT: lambda: "%s_查找类型为_%s_查找元素为_%s_操作类型为_%s" % (kw["name"],kw["find_type"], kw["element_info"],"鼠标悬浮"),
            Element.NO_OPERATE: lambda: "%s_查找类型为_%s_查找元素为_%s" % (kw["name"], kw["find_type"], kw["element_info"]),
        }
        return elements[kw["operate_type"]]()


