"""myproject02 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from myapp02 import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.base),
    path('write_form/', views.write_form),

    path('insert/', views.insert),
    path('list/', views.list),
    path('list_page/', views.list_page),
    path('download_count/', views.download_count),
    path('download/', views.download),
    path('detail_id/', views.detail_id),

    path('detail/<int:board_id>/', views.detail),
    path('update_form/<int:board_id>/', views.update_form),
    path('update/', views.update),
    path('delete/<int:board_id>/', views.delete),

]
