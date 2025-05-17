from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # API routes
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', views.get_current_user, name='get_current_user'),
    path('api/mytasks/<int:pk>/', views.update_task_status, name='update_task_status'),
    path('api/tasks/<int:pk>/report/', views.view_task_report, name='view_task_report'),
    path('api/user-tasks/', views.get_user_tasks),
    path('api/tasks/update-status/<int:pk>/', views.update_task_status),
    path('api/users/', views.user_list_create, name='user_list_create'),
    path('api/users/<int:pk>/', views.user_detail, name='user_detail'),
    path('api/tasks/admin/', views.task_list_create, name='admin_task_list_create'),
    path('api/admin/users/', views.admin_load_users, name='admin_load_users'),
    path('api/tasks/', views.task_list_create, name='task_list_create'),
    path('api/tasks/<int:pk>/', views.task_detail, name='task_detail'),

    # HTML routes
    
    path('', views.index, name='login'),
    path('my-tasks/', views.user_task_dashboard, name='user_task_dashboard'),
    path('login/', views.login_page, name='login'),
    path('superadmin/dashboard/', TemplateView.as_view(template_name='superadmin_dash.html'), name='superadmin_dashboard'),
    path('admin_dashboard/', TemplateView.as_view(template_name='admin_dash.html'), name='admin_dashboard'),
    path('user/dashboard/', TemplateView.as_view(template_name='user_dash.html'), name='user_dashboard'),
    path('users/', views.manage_users_page, name='manage_users_page'),
    path('admins/', views.manage_admin_page, name='manage_admin_page'),
    path('admin_tasks/', views.admin_task, name='admin_task'),
    path('tasks/', views.manage_tasks_page, name='manage_tasks_page'),
    path('tasks/<int:pk>/report-page/', views.task_report_page, name='task_report_page'),
]