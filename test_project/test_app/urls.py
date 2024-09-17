from django.urls import path
from .import views as v
from .api_views import CompanyQueryAPI
app_name = 'test_app'
urlpatterns = [
    path("index", v.index,  name="index"),
    path("register",v.register,name="registration"),
    path("logout",v.logout,name="logoutt"),
    path('dashboard',v.dashboard,name="dashboard"),
    path('upload_data',v.upload_data,name="upload_data"),
    path('upload_file',v.upload_file,name='upload_file'),
    path('user_list', v.user_list, name='user_list'),
    path('query-builder/', v.query_builder_view, name='query_builder'),
    path('add_user', v.add_user, name='add_user'),
    path('delete-user/<int:user_id>/', v.delete_user, name='delete_user'),
    #path('filter_data',v.filter_data,name='filter_data'),
    path('api-company-query/', CompanyQueryAPI.as_view(), name='company_query_api'),
   
]
