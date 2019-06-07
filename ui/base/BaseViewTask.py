# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
import time
import uuid
from datetime import datetime

from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from ..base import BaseLog
from ..base.BaseElementEnmu import Element
from ..base.BaseView import get_login, new_report, get_driver, new_report_item, edit_report, write_excel
from ..models import Task, Module, Case, Login, Setting
from ..base.BasePage import PagesObjects


class BaseViewTask:

    @staticmethod
    def task(request, path):
        template = loader.get_template(path)
        context = {'task_list': Task.objects.all()}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def task_new(name):
        Task(name=name).save()
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def task_edit(kw):
        id = kw["id"]
        name = kw["name"]
        ta = Task.objects.get(pk=id)
        ta.name = name
        ta.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def task_del(id):
        ta = Task.objects.get(pk=id)
        ta.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def task_run(tid):
        uid = str(uuid.uuid1())
        base_log = BaseLog.Log(uid + ".log")
        se = Setting.objects.get(pk=1)
        driver = get_driver(se.login_url)
        lg_dict = {"driver": driver, "log_test": base_log, "name": "登录",
                   "test_step": list(Login.objects.order_by("sort").values())}
        _login = get_login(lg_dict)

        if not _login:
            result = {'code': -1, 'msg': '登录失败'}
            return JsonResponse(result)

        ta = Task.objects.get(id=tid)  # 单个任务
        mo = ta.taskmodule_set.all()  # 任务下的模块
        excel_init = {}
        excel_detail = []
        passed = failed = no_check = 0
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        r_time = time.time()
        _report = new_report({"name": ta.name, "uid": uid})
        for i in mo:
            list_case = Module.objects.get(pk=i.mid).case_set.all()
            if not list_case:
                result = {'code': -1, 'msg': '无测试用例'}
                return JsonResponse(result)

            for c in list_case:
                ls_step = list(Case.objects.get(pk=c.id).steps_set.all().values())
                ls_check = list(Case.objects.get(pk=c.id).checks_set.all().values())
                if len(ls_step) == 0:
                    result = {'code': -1, 'msg': '无测试步骤'}
                    return JsonResponse(result)
                if len(ls_check) == 0:
                    result = {'code': -1, 'msg': '无检查步骤'}
                    return JsonResponse(result)
                _step = _check = ""
                for s in ls_step:
                    st = "步骤名字:%s_元素名:%s_扩展字段:%s_查找类型:%s_操作类型:%s" %(s["name"], s["element_info"], s.get("extend", "无"),
                                                                    s["find_type"], s["operate_type"])
                    _step = _step + st + "\n"
                for lc in ls_check:
                    lt = "检查点名字:%s_元素名:%s_查找类型:%s" % (lc["name"], lc["element_info"], lc["find_type"])
                    _check = _check + lt +"\n"

                page = PagesObjects({"driver": driver, "log_test": base_log, "name": c.name, "test_step": ls_step,"home_url": se.home_url,
                                     "test_check": ls_check})
                s_time = time.time()
                page.operate()
                res = page.check_point()
                e_time = time.time()
                app = {"name": c.name, "step": _step, "hope": _check, "report": _report,
                       "sum_time": "%.2f" % (e_time - s_time) + "秒", "uid": uid, "result": res}

                if res == Element.C_CHECK["passed"]:
                    passed += 1
                    base_log.build_end_line("检查点=通过")
                    base_log.check_point_ok(c.name)
                elif res == Element.C_CHECK["failed"]:
                    failed += 1
                    base_log.build_end_line("检查点=失败")
                    app["img"] = base_log.check_point_ng(driver, c.name, str(uuid.uuid1()))

                new_report_item(app)

                excel_detail.append(app)
        r_e_time = time.time()
        excel_init["start_time"] = start_time
        excel_init["sum_time"] = "%.2f" % (r_e_time - r_time) + "秒"
        excel_init["sum_case"] = passed + failed
        excel_init["passed"] = passed
        excel_init["failed"] = failed
        edit_report(
            {"sum_time": "%.2f" % (r_e_time - r_time) + "秒", "passed": passed, "failed": failed, "report": _report})
        write_excel({"uid": uid, "excel_init": excel_init, "excel_detail": excel_detail})
        result = {'code': 0, 'msg': '测试完成'}
        driver.close()
        return JsonResponse(result)
