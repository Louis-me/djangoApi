from . import views
from django.urls import path
app_name = "api"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login_edit', views.login_edit, name='login_edit'),
    path('report_del', views.report_del, name='report_del'),
    path('download_log', views.download_log, name='download_log'),
    path('download_excel', views.download_excel, name='download_excel'),
    path('<int:id>/report_detail/', views.report_detail, name='report_detail'),
    path('module', views.module, name='module'),
    path('module_new', views.module_new, name='module_new'),
    path('module_edit', views.module_edit, name='module_edit'),
    path('module_del', views.module_del, name='module_del'),
    path('<int:id>/case/', views.case, name='case'),
    path('case_new', views.case_new, name='case_new'),
    path('case_new', views.case_new, name='case_new'),
    path('case_edit', views.case_edit, name='case_edit'),
    path('case_del', views.case_del, name='case_del'),
    path('<int:mid>/<int:cid>/fuzz/', views.fuzz, name='fuzz'), # 第一个id为模块id,第二个为用例id
    path('batch_fuzz', views.batch_fuzz, name='batch_fuzz'),
    path('fuzz_new', views.fuzz_new, name='fuzz_new'),
    path('fuzz_edit', views.fuzz_edit, name='fuzz_edit'),
    path('fuzz_del', views.fuzz_del, name='fuzz_del'),
    path('task', views.task, name="task"),
    path('task_new', views.task_new, name="task_new"),
    path('task_edit', views.task_edit, name="task_edit"),
    path('task_del', views.task_del, name="task_del"),
    path('task_run', views.task_run, name="task_run"),
    path('task_module_new', views.task_module_new, name="task_module_new"),
    path('<int:id>/task_module/', views.task_module, name="task_module"),
    path('task_module_edit', views.task_module_edit, name="task_module_edit"),
    path('task_module_del', views.task_module_del, name="task_module_del")
]