# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.views.decorators.csrf import csrf_exempt
from ui.base.BaseViewTaskModule import BaseViewTaskModule
from .base.BaseViewDashBoard import BaseViewDashBoard
from .base.BaseViewLogin import BaseViewLogin
from .base.BaseViewModule import BaseViewModule
from .base.BaseViewCase import BaseViewCase
from .base.BaseViewTask import BaseViewTask
from .base.BaseViewSetting import BaseViewSetting
from .base.BaseViewStep import BaseViewStep
from .base.BaseViewCheck import BaseViewCheck
from .base.BaseReport import BaseReport
from .base.BaseViewCommonCase import BaseViewCommonCase
from .base.BaseViewCommonCaseStep import BaseViewCommonCaseStep
from .base.BaseViewCaseCommonCase import BaseViewCaseCommonCase


def setting(request):
    return BaseViewSetting.setting(request, "ui/setting.html")


@csrf_exempt
def setting_edit(request):
    home_url = request.POST["home_url"]
    login_url = request.POST["login_url"]
    kw = {"home_url": home_url, "login_url": login_url}
    return BaseViewSetting.setting_edit(kw)


# ============dashBoard Start==============
def dashBoard(request):
    return BaseViewDashBoard.dashBoard(request, "ui/dashBoard.html")


def dashBoard_module_case(request):
    return BaseViewDashBoard.dashBoard_module_case(request)


def dashBoard_top10_task(request):
    return BaseViewDashBoard.dashBoard_top10_task(request)


def dashBoard_top100_case_time(request):
    return BaseViewDashBoard.dashBoard_top100_case_time(request)


# =========dashBoard End=========


# ========测试报告 Start============
def index(request):
    page = request.GET.get('page')
    return BaseReport.index(request, page, "ui/index.html")


@csrf_exempt
def report_del(request):
    return BaseReport.report_del(request.POST["rid"])


# 测试模块的用例列表接口
def report_detail(request, id):
    return BaseReport.report_detail(request, "ui/reportDetail.html", id)


# 下载日志
@csrf_exempt
def download_log(request):
    return BaseReport.download_log(request.POST["log"])


# 下载excel
@csrf_exempt
def download_excel(request):
    return BaseReport.download_excel(request.POST["excel"])


# ===========测试报告 End============

# =====登录的用例 Start======
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


# ====登录 End==================


# =======模块 Start====================

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


# ======模块 End==============


# ======模块下用例 Start=================
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


# =====模块下用例 End===================

# ====用例下步骤 Start=====================

# 用例下的检查点
def check(request, mid, cid):
    return BaseViewCheck.check(request, "ui/check.html", mid, cid)


# 新建
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
    kw = {"chid": chid, "name": name, "element_info": element_info, "find_type": find_type,
          "operate_type": operate_type,
          "extend": extend}
    return BaseViewCheck.check_edit(kw)


@csrf_exempt
def check_del(request):
    return BaseViewCheck.check_del(request.POST["chid"])


# ========用例下检查点 End=====================


# =========用例下步骤 Start=============
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


# ======用例下步骤 End================

# ========任务 Start=================

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


# =======任务 End================


# ======任务关联模块=================
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


# ========任务关联模块 End====================


# =======公用用例 Start==========

def common_case(request):
    return BaseViewCommonCase.common_case(request, "ui/common-case.html")


@csrf_exempt
def common_case_new(request):
    return BaseViewCommonCase.common_case_new(request.POST["name"])


@csrf_exempt
def common_case_edit(request):
    id = request.POST["id"]
    name = request.POST["name"]
    return BaseViewCommonCase.common_case_edit({"id": id, "name": name})


@csrf_exempt
def common_case_del(request):
    return BaseViewCommonCase.common_case_del(request.POST["id"])


# =========公共用例 end==============

# =======公共用例下的步骤==========
def common_case_step(request, id):
    # id 是公共用例表的id,common_case
    return BaseViewCommonCaseStep.common_case_step(request, "ui/common-case-step.html", id)


@csrf_exempt
def common_case_step_new(request):
    cc_id = request.POST["cc_id"]
    name = request.POST["name"]
    element_info = request.POST["element_info"]
    find_type = request.POST["find_type"]
    operate_type = request.POST["operate_type"]
    extend = request.POST.get("extend", "0")
    sort = request.POST.get("sort", 0)

    kw = {"cc_id": cc_id, "name": name, "element_info": element_info, "find_type": find_type,
          "operate_type": operate_type,
          "extend": extend, "sort": sort}
    return BaseViewCommonCaseStep.common_case_step_new(kw)


@csrf_exempt
def common_case_step_edit(request):
    ccs_id = request.POST["ccs_id"]
    name = request.POST["name"]
    element_info = request.POST["element_info"]
    find_type = request.POST["find_type"]
    operate_type = request.POST["operate_type"]
    extend = request.POST.get("extend", "0")
    sort = request.POST.get("sort", 0)
    kw = {"ccs_id": ccs_id, "name": name, "element_info": element_info, "find_type": find_type,
          "operate_type": operate_type,
          "extend": extend, "sort": sort}
    return BaseViewCommonCaseStep.common_case_step_edit(kw)


@csrf_exempt
def common_case_step_del(request):
    ccs_id = request.POST["ccs_id"]
    return BaseViewCommonCaseStep.common_case_step_del(ccs_id)


# ===========公共用例下的步骤End ===========


# ======用例步骤下关联公共用例 Start===========
def case_common_case(request, mid, cid):
    # mid 模块id
    # cid 用例case表id
    return BaseViewCaseCommonCase.case_common_case(request, "ui/case-common-case.html", mid, cid)


@csrf_exempt
def case_common_case_new(request):
    cid = request.POST["cid"]  # 用例case表的id
    cc_id = request.POST["cc_id"]  # 公共用例common_case表的id
    name = request.POST["name"]
    sort = request.POST["sort"]
    kw = {"cid": cid, "cc_id": cc_id, "name": name, "sort": sort}
    return BaseViewCaseCommonCase.case_common_case_new(kw)


@csrf_exempt
def case_common_case_edit(request):
    ccc_id = request.POST["ccc_id"]
    name = request.POST["name"]
    sort = request.POST["sort"]
    cc_id = request.POST["cc_id"]  # 公共用例common_case表的id

    kw = {"ccc_id": ccc_id, "name": name, "sort": sort, "cc_id": cc_id}
    return BaseViewCaseCommonCase.case_common_case_edit(kw)


@csrf_exempt
def case_common_case_del(request):
    ccs_id = request.POST["ccc_id"]
    return BaseViewCaseCommonCase.case_common_case_del(ccs_id)

# ==========用例步骤下关联公共用例 End===============
