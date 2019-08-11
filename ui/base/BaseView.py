# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from datetime import datetime
import xlsxwriter
from selenium import webdriver
from ..base.BaseElementEnmu import Element
from ..base.BaseExcel import OperateReport
from ..base.BaseFile import BaseFile
from ..models import Report
import os
from .BasePage import PagesObjects

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def get_driver(login_url):
    chrome_driver = PATH("../lib/chromedriver.exe")
    os.environ["webdriver.chrome.driver"] = chrome_driver
    driver = webdriver.Chrome(chrome_driver)
    driver.maximize_window()  # 将浏览器最大化
    driver.get(login_url)
    return driver


def get_login(kw):
    app = {"log_test": kw["log_test"], "driver": kw["driver"], "name": kw["name"], "test_step": [kw["test_step"]]}
    page = PagesObjects(app)
    return page.operate()


'''
新建测试报告
name
uid
'''


def new_report(kw):
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _report = Report(name=kw["name"], start_time=start_time, report_path=kw["uid"], log=kw["uid"])
    _report.save()
    return _report


'''
编辑测试报告模块
report : model
'''


def edit_report(kw):
    kw["report"].sum_time = kw["sum_time"]
    kw["report"].passed = kw["passed"]
    kw["report"].failed = kw["failed"]
    # kw["report"].no_check = kw["no_check"]
    kw["report"].save()


'''
新建测试报告详情
report : model report
'''


def new_report_item(kw):
    kw["report"].reportitem_set.create(name=kw["name"], step=kw["step"], hope=kw["hope"], sum_time=kw["sum_time"],
                                       result=kw['result'], img=kw.get("img2", "0"), extend=kw["extend"])

'''
生成excel报告
'''


def write_excel(kw):
    bf = BaseFile()
    files = Element.REPORT_FILE + "\\" + kw["uid"] + ".xlsx"
    bf.mk_file(files)

    workbook = xlsxwriter.Workbook(files, {"string_to_urls": False})
    worksheet1 = workbook.add_worksheet("测试总况")
    op_report = OperateReport(workbook)
    op_report.init(worksheet1, kw["excel_init"])
    worksheet2 = workbook.add_worksheet("测试详情")
    op_report.detail(worksheet2, kw["excel_detail"])
    op_report.close()
