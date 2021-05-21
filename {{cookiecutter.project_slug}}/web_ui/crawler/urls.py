from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='status'),
    path('spiders/<str:spider>/run', views.run_spider, name='run_spider'),
    path('spiders/<str:spider>/jobs/<str:job_id>/log', views.log_detail, name='log_detail'),
    path('spiders/<str:spider>/jobs/<str:job_id>/stats', views.log_stats, name='log_stats'),
    path('stop-job/<str:job_id>', views.cancel_job, name='stop_job'),
]