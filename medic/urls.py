from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.user_signup, name='signup'),
	path('login/', views.user_login, name='user_login'),
	path('logout/', views.user_logout, name='user_logout'),
	path('add_medical_info/', views.add_analysis, name="add_medical_info"),
	path('analysis_data/', views.display_data, name="analysis_data"),
	path('high_class_chart/', views.high_class_chart, name='high_class_chart')
]