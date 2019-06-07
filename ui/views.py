# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.views.decorators.csrf import csrf_exempt
from ui.base.BaseViewTaskModule import BaseViewTaskModule
from .base.BaseViewDashboard import BaseViewDashboard
from .base.BaseViewLogin import BaseViewLogin
from .base.BaseViewModule import BaseViewModule
from .base.BaseViewCase import BaseViewCase
from .base.BaseViewTask import BaseViewTask
from .base.BaseViewSetting import BaseViewSetting
from .base.BaseViewStep import BaseViewStep
from .base.BaseViewCheck import BaseViewCheck


def setting(request):
    return BaseViewSetting.setting(request, "ui/setting.html")


@csrf_exempt
def setting_edit(request):
    home_url = request.POST["home_url"]
    login_url = request.POST["login_url"]
    kw = {"home_url": home_url, "login_url": login_url}
    return BaseViewSetting.setting_edit(kw)


def index(request):
    page = request.GET.get('page')
    return BaseViewDashboard.index(request, page, "ui/index.html")


@csrf_exempt
def report_del(request):
    return BaseViewDashboard.report_del(request.POST["rid"])


# 测试模块的用例列表接口
def report_detail(request, id):
    return BaseViewDashboard.report_detail(request, "ui/reportDetail.html", id)


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
    return BaseViewLogin.login(request, "ui/login.html")


@csrf_exempt
def login_new(request):
    find_type = request.POST["find_type"]
    element_info = request.POST["element_info"]
    operate_type = request.POST["operate_type"]
    extend = request.POST["extend"]
    sort = request.POST["sort"]
    name = request.POST["name"]
    kw = {"find_type": find_type, "element_info": element_info, "name": name, "operate_type": operate_type,
          "extend": extend, "sort": sort}
    return BaseViewLogin.login_new(kw)


# 编辑登录接口参数
@csrf_exempt
def login_edit(request):
    id = request.POST["id"]
    find_type = request.POST["find_type"]
    element_info = request.POST["element_info"]
    operate_type = request.POST["operate_type"]
    extend = request.POST["extend"]
    sort = request.POST["sort"]
    name = request.POST["name"]
    app = {"id": id, "find_type": find_type, "element_info": element_info, "operate_type": operate_type,
           "extend": extend, "sort": sort, "name": name}
    return BaseViewLogin.login_edit(app)


@csrf_exempt
def login_del(request):
    return BaseViewLogin.login_del(request.POST["id"])


# 模块列表
def module(request):
    return BaseViewModule.module(request, "ui/module.html")


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
    id = request.POST["id"]
    return BaseViewModule.module_del(id)


# 模块下的用例列表
def case(request, mid):
    return BaseViewCase.case(request, 'ui/case.html', mid)


# 新建用例
@csrf_exempt
def case_new(request):
    mid = request.POST["mid"]
    name = request.POST["name"]
    return BaseViewCase.case_new({"mid": mid, "name": name})


# 编辑用例
@csrf_exempt
def case_edit(request):
    c_id = request.POST["cid"]
    name = request.POST["name"]

    return BaseViewCase.case_edit(
        {"cid": c_id, "name": name})


# 删除用例
@csrf_exempt
def case_del(request):
    return BaseViewCase.case_del(request.POST["cid"])


# 用例下的步骤
def check(request, mid, cid):
    return BaseViewCheck.check(request, "ui/check.html", mid, cid)


# 新建步骤
@csrf_exempt
def check_new(request):
    cid = request.POST["cid"]
    name = request.POST["name"]
    element_info = request.POST["element_info"]
    find_type = request.POST["find_type"]
    operate_type = request.POST["operate_type"]
    extend = request.POST.get("extend", "")
    kw = {"cid": cid, "name": name, "element_info": element_info, "find_type": find_type, "operate_type": operate_type,
          "extend": extend}
    return BaseViewCheck.check_new(kw)


@csrf_exempt
def check_edit(request):
    chid = request.POST["chid"]
    name = request.POST["name"]
    element_info = request.POST["element_info"]
    find_type = request.POST["find_type"]
    operate_type = request.POST["operate_type"]
    extend = request.POST.get("extend", "")
    kw = {"chid": chid, "name": name, "element_info": element_info, "find_type": find_type, "operate_type": operate_type,
          "extend": extend}
    return BaseViewCheck.check_edit(kw)


@csrf_exempt
def check_del(request):
    return BaseViewCheck.check_del(request.POST["chid"])


# 用例下的步骤
def step(request, mid, cid):
    return BaseViewStep.step(request, "ui/step.html", mid, cid)


# 新建步骤
@csrf_exempt
def step_new(request):
    cid = request.POST["cid"]
    name = request.POST["name"]
    element_info = request.POST["element_info"]
    find_type = request.POST["find_type"]
    operate_type = request.POST["operate_type"]
    extend = request.POST.get("extend", "无")
    sort = request.POST.get("sort", 0)
    kw = {"cid": cid, "name": name, "element_info": element_info, "find_type": find_type, "operate_type": operate_type,
          "extend": extend, "sort": sort}
    return BaseViewStep.step_new(kw)


@csrf_exempt
def step_edit(request):
    sid = request.POST["sid"]
    name = request.POST["name"]
    element_info = request.POST["element_info"]
    find_type = request.POST["find_type"]
    operate_type = request.POST["operate_type"]
    extend = request.POST.get("extend", "无")
    sort = request.POST.get("sort", "")

    kw = {"sid": sid, "name": name, "element_info": element_info, "find_type": find_type, "operate_type": operate_type,
          "extend": extend, "sort": sort}
    return BaseViewStep.step_edit(kw)


@csrf_exempt
def step_del(request):
    return BaseViewStep.step_del(request.POST["sid"])


def task(request):
    return BaseViewTask.task(request, "ui/task.html")


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
    return BaseViewTaskModule.task_module(request, "ui/taskModule.html", id)


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
