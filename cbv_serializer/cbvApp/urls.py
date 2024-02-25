from django.urls import path
from . import views

urlpatterns = [
    path('',views.StudentList.as_view()),
    path('<int:pk>/',views.StudentDetails.as_view()),
]
