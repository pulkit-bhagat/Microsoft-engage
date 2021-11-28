from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registerteacher/', views.registerTeacher, name='register-teacher'),
    path('loginteacher/', views.loginTeacher, name='login-teacher'),
    path('logout/', views.logoutUser, name='logout'),
    path('addcourse/', views.addCourse, name='add-course'),
    path('registerstudent/', views.registerStudent, name='register-student'),
    path('loginstudent/', views.loginStudent, name='login-student'),
    path('enrollcourse/', views.enrollCourse, name='enroll-course'),
    path('tclassroom/<str:pk>/', views.tClassroom, name='t-classroom'),
    path('sclassroom/<str:pk>/', views.sClassroom, name='s-classroom'),
    path('submitupdate/<str:pk>/', views.submitUpdate, name='submit-update'),
    path('createassignment/<str:pk>/', views.createAssignment, name='create-assignment'),
    path('assignment/<int:pk>/', views.assignment, name='assignment'),
    path('score/<int:pk>/<str:username>/', views.submitScore, name='submit-score'),
    path('setclasstime/<str:pk>/', views.setClassTime, name='set-class-time'),
    
]
