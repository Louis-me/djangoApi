from . import views
from django.urls import path

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
    path('<int:id>/fuzz/', views.fuzz, name='fuzz'),
    path('batch_fuzz', views.batch_fuzz, name='batch_fuzz'),
    path('fuzz_new', views.fuzz_new, name='fuzz_new'),
    path('fuzz_edit', views.fuzz_edit, name='fuzz_edit'),
    path('fuzz_del', views.fuzz_del, name='fuzz_del'),
    path('run', views.run, name='run')
    # path('module', views)
]