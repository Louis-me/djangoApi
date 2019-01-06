import ast
import json
from datetime import datetime

import requests
import xlsxwriter

from api.base.BaseElementEnmu import Element
from api.base.BaseExcel import OperateReport
from api.base.BaseFile import BaseFile
from api.models import Login, Report

'''
登录
'''


def get_session():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

    s = requests.session()
    l = Login.objects.get(pk=1)
    url = l.url
    data = json.loads(l.params)
    # s.post(url, data, verify=False)
    s.post(url, data, headers=headers, verify=False)
    return s


'''
检查点
kw[hope]|'{"a": "b"}'
kw[fact]|
a1 = '{"a": "b", "c": "d"}'   直接找值
a2 = '{"a": "b", "c": "d", "data":{"a": "b1"}}' 找data里面的值
a3 = '[{"a":"b"},{"c":"d"}]' 找list重dict里的值
'''


def _check(kw):
    if len(kw["hope"]) == 0 or len(kw["fact"]) == 0:
        return Element.C_CHECK["no_check"]
    print("===value=%s=type=%s=" % (kw["fact"], type(kw["fact"])))
    hope = ast.literal_eval(kw["hope"])
    fact = ast.literal_eval(kw["fact"])
    # hope = ast.literal_eval(kw["hope"])
    # fact = ast.literal_eval(kw["fact"])
    if type(fact) == dict:
        for items in fact:
            if type(fact[items]) == dict:
                for k in hope:
                    if fact[items].get(k, "") == hope[k]:
                        return Element.C_CHECK["passed"]
            for k in hope:
                if fact.get(k, "") == hope[k]:
                    return Element.C_CHECK["passed"]
    elif type(fact) == list:
        for i in fact:
            print(i)
            for k in hope:
                if i.get(k, "") == hope[k]:
                    return Element.C_CHECK["passed"]
    return Element.C_CHECK["failed"]


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
    kw["report"].no_check = kw["no_check"]
    kw["report"].save()


'''
新建测试报告详情
report : model report
name
url
protocol
method
params
hope
sum_time
fact
result
'''


def new_report_item(kw):
    kw["report"].reportitem_set.create(name=kw["name"], url=kw["url"], protocol=kw["protocol"], code=kw["code"],
                                       method=kw["method"], params=kw["params"], hope=kw.get("hope", ""),
                                       sum_time=kw["sum_time"], fact=kw["fact"], result=kw['result']).save()


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

