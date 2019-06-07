# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Report
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from djangoApi import settings
import os


class BaseViewDashboard:

    @staticmethod
    def index(request, page, path):
        list_report = Report.objects.order_by('-id')
        template = loader.get_template(path)
        paginator = Paginator(list_report, 8, 2)  # 每页8条数据，少于2条则合并到上一页

        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)

        context = {
            "list_report": customer
        }
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def report_del(id):
        Report.objects.get(pk=id).delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)

    @staticmethod
    def report_detail(request, path, id):
        rp = Report.objects.get(pk=id)
        template = loader.get_template(path)
        context = {'case_list': rp.reportitem_set.all(), "id": id, "name": rp.name}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def download_log(file_path):
        def file_iterator(file_name, chunk_size=2612000):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        file_name = os.path.join(settings.BASE_DIR, "ui/Log", file_path + ".log")
        http_file = "http://192.168.56.1:8001/ui/Log/" + file_path + ".log"
        # 192.168.1.100:8001在apache中设置
        response = HttpResponse(file_iterator(file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("report.log")
        result = {'code': 0, 'msg': '下载成功', "path": http_file}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def download_excel(file_path):
        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        file_name1 = os.path.join(settings.BASE_DIR, "ui/Report", file_path + ".xlsx")
        http_file = "http://192.168.56.1:8001/ui/Report/" + file_path + ".xlsx"
        response = HttpResponse(file_iterator(file_name1))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("report.xlsx")
        result = {'code': 0, 'msg': '下载成功', "path": http_file}
        return JsonResponse(result)



