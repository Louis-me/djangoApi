import ast
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from api.base.BaseElementEnmu import Element
from api.base.BaseView import new_report_item, edit_report, write_excel, get_session, new_report, _check
from ..models import Module, Case
import json
import time
from datetime import datetime
import uuid
from ..base import BaseLog
import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

class BaseViewModule:

    @staticmethod
    def module(request, path):
        template = loader.get_template(path)
        context = {'module_list': Module.objects.all()}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def module_new(name):
        Module(name=name).save()
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def module_edit(kw):
        m_id = kw["id"]
        name = kw["name"]
        m = Module.objects.get(pk=m_id)
        m.name = name
        m.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def module_del(id):
        m = Module.objects.get(pk=id)
        m.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
    
    @staticmethod
    @csrf_exempt
    def run(mid):
        list_case = Module.objects.get(pk=mid).case_set.all()
        if not list_case:
            result = {'code': -1, 'msg': '无测试用例'}
            return JsonResponse(result)
        excel_init = {}
        excel_detail = []
        uid = str(uuid.uuid1())
        base_log = BaseLog.Log(uid + ".log")
        req = get_session()
        passed = failed = no_check = 0
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        _report = new_report({"name": Module.objects.get(pk=mid).name, "uid": uid})
        for c in list_case:
            ls_fuzz = Case.objects.get(pk=c.id).fuzzcase_set.all()

            r_time = time.time()
            if ls_fuzz:  # 如果用模糊用例
                print("=====有模糊用例====")
                for fu in ls_fuzz:
                    s_time = int(round(time.time() * 1000))
                    resp = ""
                    if fu.method == "post":
                        data = ast.literal_eval(fu.params)
                        resp = req.post(url=fu.protocol + "://" + fu.url, data=data)
                        base_log.buildStartLine("请求url=%s" % resp.url)
                        base_log.buildStartLine("请求参数=%s" % fu.params)
                    if fu.method == "get":
                        resp = req.get(url=fu.protocol + "://" + fu.url, params=ast.literal_eval(fu.params))
                        base_log.buildStartLine("请求url=%s" % resp.url)
                        base_log.buildStartLine("请求参数=%s" % fu.params)
                    e_time = int(round(time.time() * 1000))
                    f_result = _check({"hope": fu.hope, "fact": resp.text})
                    app = {"name": fu.name, "url": resp.url, "protocol": fu.protocol, "report": _report,
                           "method": fu.method, "params": fu.params, "hope": fu.hope,
                           "sum_time": str(e_time - s_time) + "ms",
                           "fact": resp.text, "uid": uid, "result": f_result, "code": resp.status_code}
                    no_check += 1
                    new_report_item(app)
                    repo_item = {"url": resp.url, "method": fu.method, "params": fu.params, "name": fu.name,
                                 "hope": fu.hope,
                                 "code": resp.status_code, "fact": resp.text, "result":f_result,
                                 "sum_time": str(e_time - s_time) + "ms"}
                    excel_detail.append(repo_item)

            res = ""
            ss_time = int(round(time.time() * 1000))
            if c.method == "post":
                res = req.post(url=c.protocol + "://" + c.url, data=json.dumps(c.params))
                base_log.buildStartLine("请求url=%s" % res.url)
                base_log.buildStartLine("请求参数=%s" % c.params)
            if c.method == "get":
                res = req.get(url=c.protocol + "://" + c.url, params=ast.literal_eval(c.params))
                base_log.buildStartLine("请求url=%s" % res.url)
                base_log.buildStartLine("请求参数=%s" % c.params)
            ee_time = int(round(time.time() * 1000))
            _result = _check({"hope": c.hope, "fact": res.text})
            if _result == Element.C_CHECK["passed"]:
                passed += 1
                base_log.buildEndLine("检查点=通过")
            elif _result == Element.C_CHECK["failed"]:
                failed += 1
                base_log.buildEndLine("检查点=失败")

            app = {"report": _report, "name": c.name, "url": res.url, "protocol": c.protocol, "method": c.method,
                   "code": res.status_code,
                   "params": c.params, "hope": c.hope, "sum_time": str(ee_time - ss_time) + "ms", "fact": res.text,
                   "result": _result}
            new_report_item(app)
            r_e_time = time.time()
            edit_report({"sum_time": "%.2f" % (r_e_time - r_time) + "秒", "passed": passed, "failed": failed,
                         "no_check": no_check, "report": _report})

            # report_init
            excel_init["start_time"] = start_time
            excel_init["sum_time"] = "%.2f" % (r_e_time - r_time) + "秒"
            excel_init["sum_case"] = passed + failed + no_check
            excel_init["passed"] = passed
            excel_init["failed"] = failed
            excel_init["no_check"] = no_check

            # report_detail
            repo_item = {"url": res.url, "method": c.method, "params": c.params, "name": c.name, "hope": c.hope,
                         "code": res.status_code, "fact": res.text, "result": _result,
                         "sum_time": str(ee_time - ss_time) + "ms"}
            excel_detail.append(repo_item)

        result = {'code': 0, 'msg': '测试完成'}
        write_excel({"uid": uid, "excel_init": excel_init, "excel_detail": excel_detail})
        return JsonResponse(result)

    
