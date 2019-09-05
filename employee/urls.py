from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('emp', views.emp),
    path('show', views.show),
    # path('edit/<int:id>', views.edit),
    # path('update/<int:id>', views.update),
    # path('hike', views.hike),
    path('employee_hike', views.employee_hike),
]