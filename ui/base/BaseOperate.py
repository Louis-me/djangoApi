# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
from .BaseElementEnmu import Element as be
from selenium.webdriver.common.action_chains import *
import time
import re

'''
# 此脚本主要用于查找元素是否存在，操作页面元素
'''


class OperateElement:
    def __init__(self, driver=""):
        self.driver = driver

    def find_element(self, operate):
        '''
        查找元素.operate,dict|list
        operate_type：对应的操作
        element_info：元素详情
        find_type: find类型
        '''
        try:
            t = operate["check_time"] if operate.get("check_time",
                                                     "0") != "0" else be.WAIT_TIME  # 如果自定义检测时间为空，就用默认的检测等待时间
            if type(operate) == list:  # 多检查点
                for item in operate:
                    t = item["check_time"] if item.get("check_time", "0") != "0" else be.WAIT_TIME
                    WebDriverWait(self.driver, t).until(lambda x: self.elements_by(item))
                return {"result": True}
            if type(operate) == dict:  # 单检查点
                if operate.get("element_info", "0") == "0":  # 如果没有页面元素，就不检测是页面元素，可能是滑动等操作
                    return {"result": True}
                WebDriverWait(self.driver, t).until(lambda x: self.elements_by(operate))
                return {"result": True}
        except selenium.common.exceptions.TimeoutException:
            return {"result": False, "type": be.TIME_OUT}
        except selenium.common.exceptions.NoSuchElementException:
            return {"result": False, "type": be.NO_SUCH}
        except selenium.common.exceptions.WebDriverException:
            return {"result": False, "type": be.WEB_DROVER_EXCEPTION}

    '''
    查找元素.mOperate是字典:operate_type,element_info,find_type:
    name: 用例介绍
    log_test: 记录日志
    '''

    def operate(self, operate, test_case, log_test):
        res = self.find_element(operate)
        if res["result"]:
            return self.operate_by(operate, test_case, log_test)
        else:
            return res

    def __time(self, operate):
        if operate.get("extend", "none") == "time":
            time.sleep(1)

    def operate_by(self, operate, name, log_test):

        try:
            info = "%s_%s_%s_%s" % (
                operate.get("element_info", " "), operate.get("find_type"), operate.get("operate_type", " "),
                operate.get("extend", " "))
            print("==操作步骤：%s==" % info)
            log_test.build_start_line(name + "_" + info)  # 记录日志

            if operate.get("operate_type", "0") == "0":  # 如果没有此字段，说明没有相应操作，一般是检查点，直接判定为成功
                return {"result": True}
            elements = {
                be.CLICK: lambda: self.click(operate),
                be.GET_VALUE: lambda: self.get_value(operate),
                be.GET_TEXT: lambda: self.get_text(operate),
                be.SEND_KEYS: lambda: self.send_keys(operate),
                be.SWITCH_TO_DEFAULT_CONTENT: lambda: self.switch_to_default_content(),
                be.SWITCH_TO_WINDOW: lambda: self.switch_to_window(operate),
                be.SWITCH_TO_FRAME: lambda: self.switch_to_frame(operate),
            }
            return elements[operate.get("operate_type")]()
        except IndexError:
            return {"result": False, "type": be.INDEX_ERROR}
        except selenium.common.exceptions.NoSuchElementException:
            return {"result": False, "type": be.NO_SUCH}
        except selenium.common.exceptions.StaleElementReferenceException:
            return {"result": False, "type": be.STALE_ELEMENT_REFERENCE_EXCEPTION}
        except KeyError:
            # 如果key不存在，一般都是在自定义的page页面去处理了，这里直接返回为真
            return {"result": True}

    # 点击事件
    def click(self, operate):
        if operate["find_type"] == be.find_element_by_id or operate["find_type"] == be.find_element_by_xpath \
                or be.find_element_by_css_selector or operate["find_type"] == be.find_element_by_class_name or \
                operate["find_type"] == be.find_element_by_link_text:
            self.elements_by(operate).click()
            # self.driver.execute_script("arguments[0].click();", self.elements_by(operate))
            self.__time(operate)
        return {"result": True}

    def send_keys(self, operate):
        """
        :param operate:
        :return:
        """
        self.elements_by(operate).send_keys(operate["extend"])
        return {"result": True}

    def get_text(self, operate):
        '''
        :param operate:
        :return: {}
        '''

        if operate.get("find_type") == be.find_elements_by_id:
            element_info = self.elements_by(operate)[operate["extend"]]

            result = element_info.get_attribute("text")
            re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)  # 只匹配中文，大小写，字母
            return {"result": True, "text": "".join(re_reulst)}

        element_info = self.elements_by(operate)
        result = element_info.get_attribute("text")

        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return {"result": True, "text": "".join(re_reulst)}

    def get_value(self, operate):
        if operate.get("find_type") == be.find_elements_by_id:
            element_info = self.elements_by(operate)[operate["index"]]

            result = element_info.get_attribute("value")
            re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)  # 只匹配中文，大小写，字母
            return {"result": True, "text": "".join(re_reulst)}

        element_info = self.elements_by(operate)
        result = element_info.get_attribute("value")

        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return {"result": True, "text": "".join(re_reulst)}

    '''
    鼠标悬停
    '''

    def move_to_element(self, operate):
        ActionChains(self.driver).move_to_element(self.elements_by(operate)).perform()
        return {"result": True}

    # 切换窗口
    def switch_to_window(self, operate):
        self.driver.switch_to.window(operate["extend"])

    # 一般切换到iframe后，可以用此函数切换到最外层
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def switch_to_frame(self, operate):
        self.driver.switch_to.frame(operate["extend"])

    # 封装常用的标签
    def elements_by(self, operate):
        elements = {
            be.find_element_by_id: lambda: self.driver.find_element_by_id(operate["element_info"]),
            be.find_element_by_xpath: lambda: self.driver.find_element_by_xpath(operate["element_info"]),
            be.find_element_by_class_name: lambda: self.driver.find_element_by_class_name(operate['element_info']),
            be.find_elements_by_id: lambda: self.driver.find_elements_by_id(operate['element_info']),
            be.find_element_by_css_selector: lambda: self.driver.find_element_by_css_selector(operate['element_info']),
            be.find_element_by_link_text: lambda: self.driver.find_element_by_link_text(operate['element_info']),
            be.find_element_by_name: lambda: self.driver.find_element_by_name(operate['element_info'])

        }
        return elements[operate["find_type"]]()
