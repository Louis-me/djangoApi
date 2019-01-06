from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from api.base.BaseViewTaskModule import BaseViewTaskModule
from .base.BaseViewDashboard import BaseViewDashboard
from .base.BaseViewLogin import BaseViewLogin
from .base.BaseViewModule import BaseViewModule
from .base.BaseViewCase import BaseViewCase
from .base.BaseViewFuzz import BaseViewFuzz
from .base.BaseViewTask import BaseViewTask


def index(request):
    page = request.GET.get('page')
    return BaseViewDashboard.index(request, page, "api/index.html")


@csrf_exempt
def report_del(request):
    return BaseViewDashboard.report_del(request.POST["rid"])


# 测试模块的用例列表接口
def report_detail(request, id):
    return BaseViewDashboard.report_detail(request, "api/reportDetail.html", id)


# 下载日志
@csrf_exempt
def download_log(request):
    return BaseViewDashboard.download_log(request.POST["log"])


# 下载excel
@csrf_exempt
def download_excel(request):
    return BaseViewDashboard.download_excel(request.POST["excel"])


# 接口测试需要登录
def login(request):
    return BaseViewLogin.login(request, "api/login.html")


# 编辑登录接口参数
@csrf_exempt
def login_edit(request):
    url = request.POST["url"]
    params = request.POST["params"]
    return BaseViewLogin.login_edit({"url": url, "params": params})


# 模块列表
def module(request):
    return BaseViewModule.module(request, "api/module.html")


@csrf_exempt
def module_new(request):
    return BaseViewModule.module_new(request.POST["name"])


# 编辑模块
@csrf_exempt
def module_edit(request):
    m_id = request.POST["id"]
    name = request.POST["name"]
    return BaseViewModule.module_edit({"id": m_id, "name": name})


# 删除模块
@csrf_exempt
def module_del(request):
    m_id = request.POST["mid"]
    return BaseViewModule.module_del(m_id)


@csrf_exempt
def run(request):
    return BaseViewModule.run(request.POST["mid"])

# 模块下的用例列表
def case(request, id):
    return BaseViewCase.case(request, 'api/case.html', id)


# 新建用例
@csrf_exempt
def case_new(request):
    id = request.POST["mid"]
    name = request.POST["name"]
    url = request.POST["url"]
    protocol = request.POST["protocol"]
    method = request.POST["method"]
    params = request.POST["params"]
    hope = request.POST.get("hope", "")
    return BaseViewCase.case_new(
        {"mid": id, "name": name, "url": url, "protocol": protocol, "method": method, "params": params, "hope": hope})


# 编辑用例
@csrf_exempt
def case_edit(request):
    c_id = request.POST["cid"]
    name = request.POST["name"]
    url = request.POST["url"]
    protocol = request.POST["protocol"]
    method = request.POST["method"]
    params = request.POST["params"]
    hope = request.POST["hope"]
    return BaseViewCase.case_edit(
        {"cid": c_id, "name": name, "url": url, "protocol": protocol, "method": method, "params": params, "hope": hope})


# 删除用例
@csrf_exempt
def case_del(request):
    return BaseViewCase.case_del(request.POST["cid"])


# 模糊用列表
def fuzz(request, mid, cid):
    return BaseViewFuzz.fuzz(request, "api/fuzz.html", mid, cid)


# 生成模糊用例
@csrf_exempt
def batch_fuzz(request):
    return BaseViewFuzz.batch_fuzz(request.POST["cid"])


# 新建模糊用例
@csrf_exempt
def fuzz_new(request):
    cid = request.POST["cid"]
    name = request.POST["name"]
    url = request.POST["url"]
    protocol = request.POST["protocol"]
    method = request.POST["method"]
    params = request.POST["params"]
    hope = request.POST.get("hope", "")
    return BaseViewFuzz.fuzz_new(
        {"cid": cid, "name": name, "url": url, "protocol": protocol, "method": method, "params": params, "hope": hope})


# 编辑模糊用例
@csrf_exempt
def fuzz_edit(request):
    fid = request.POST["fid"]
    name = request.POST["name"]
    url = request.POST["url"]
    protocol = request.POST["protocol"]
    method = request.POST["method"]
    params = request.POST["params"]
    hope = request.POST["hope"]
    return BaseViewFuzz.fuzz_edit(
        {"fid": fid, "name": name, "url": url, "protocol": protocol, "method": method, "params": params, "hope": hope})


# 删除模糊用例
@csrf_exempt
def fuzz_del(request):
    fid = request.POST["fid"]
    return BaseViewFuzz.fuzz_del(fid)


def task(request):
    return BaseViewTask.task(request, "api/task.html")


@csrf_exempt
def task_new(request):
    name = request.POST["name"]
    return BaseViewTask.task_new(name)


@csrf_exempt
def task_edit(request):
    name = request.POST["name"]
    id = request.POST["id"]
    return BaseViewTask.task_edit({"name": name, "id": id})


@csrf_exempt
def task_del(request):
    id = request.POST["id"]
    return BaseViewTask.task_del(id)


@csrf_exempt
def task_run(request):
    return BaseViewTask.task_run(request.POST["tid"])


def task_module(request, id):
    return BaseViewTaskModule.task_module(request, "api/taskModule.html", id)


@csrf_exempt
def task_module_new(request):
    tid = request.POST["tid"]
    mid = request.POST["mid"]
    # name = request.POST.getlist("mid")
    name = request.POST["name"]
    return BaseViewTaskModule.task_module_new(tid, name, mid)


@csrf_exempt
def task_module_edit(request):
    tmid = request.POST["tmid"]
    mid = request.POST["mid"]
    name = request.POST["name"]
    return BaseViewTaskModule.task_module_edit({"tmid": tmid, "mid": mid, "name": name})


@csrf_exempt
def task_module_del(request):
    return BaseViewTaskModule.task_module_del(request.POST["tmid"])
