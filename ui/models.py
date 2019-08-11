# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.db import models


class Setting(models.Model):
    login_url = models.CharField(max_length=200)
    home_url = models.CharField(max_length=200)


class Login(models.Model):
    element_info = models.CharField(max_length=300)
    find_type = models.CharField(max_length=300)
    operate_type = models.CharField(max_length=100)
    extend = models.CharField(max_length=100)
    sort = models.IntegerField(default=0)
    name = models.CharField(max_length=100)


class Report(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    sum_time = models.CharField(max_length=10)
    passed = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    no_check = models.IntegerField(default=0)
    log = models.CharField(max_length=100, null=True)
    report_path = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ReportItem(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    step = models.CharField(max_length=300)
    hope = models.CharField(max_length=100)
    sum_time = models.CharField(max_length=50)
    result = models.IntegerField(default=0)  # 0通过，-1失败，-2不检查
    img = models.CharField(max_length=100, default="")
    extend = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Case(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Steps(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    element_info = models.CharField(max_length=300)
    find_type = models.CharField(max_length=300)
    operate_type = models.CharField(max_length=100)
    extend = models.CharField(max_length=100)
    sort = models.IntegerField(default=0)


class Checks(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    element_info = models.CharField(max_length=300)
    find_type = models.CharField(max_length=300)
    operate_type = models.CharField(max_length=100)
    extend = models.CharField(max_length=100)


class Task(models.Model):
    name = models.CharField(max_length=100, default="")


# 关联任务和模块
class TaskModule(models.Model):
    mid = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


# 公共用例
class CommonCase(models.Model):
    name = models.CharField(max_length=100, default="")


# 公共用例步骤
class CommonCaseStep(models.Model):
    commonCase = models.ForeignKey(CommonCase, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    element_info = models.CharField(max_length=300)
    find_type = models.CharField(max_length=300)
    operate_type = models.CharField(max_length=100)
    extend = models.CharField(max_length=100)
    sort = models.IntegerField(default=0)


# 用例关联公共用例
class CaseCommonCase(models.Model):
    cc_id = models.IntegerField(default=0)  # 公共用例 的id
    name = models.CharField(max_length=100)
    sort = models.IntegerField(default=0)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, default=0)
