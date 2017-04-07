'''
Created on 10-Sep-2015

@author: utkarsh
'''
from django.conf.urls import url
from instagram_service.service_apis.best_time_to_post import BestTimeToPost

urlpatterns = [
    url(r'^find/best-time-to-post/$', BestTimeToPost.as_view()), 
]
