from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectList.as_view(), name='project_list'),
    path('project/create/', views.ProjectCreate.as_view(), name='project_create'),
    path('project/<int:pk>/', views.ProjectDetail.as_view(), name='project_detail'),
    path('project/edit/<int:pk>/', views.ProjectUpdate.as_view(), name='project_edit'),
    path('project/duplicate/<int:pk>/', views.ProjectDuplicate.as_view(), name='project_duplicate'),
    path('project/delete/<int:pk>/', views.ProjectDelete.as_view(), name='project_delete'),
    path('map/create/', views.MapCreate.as_view(), name='map_create'),
    path('map/<int:pk>/', views.MapDetail.as_view(), name='map_detail'),
    path('map/array/<int:pk>/', views.MapArray.as_view(), name='map_array'),
    path('map/split/<int:pk>/', views.MapSplit.as_view(), name='map_split'),
    path('map/timeseries/<int:pk>/', views.MapTimeSeries.as_view(), name='map_split'),
    path('map/edit/<int:pk>/', views.MapUpdate.as_view(), name='map_edit'),
    path('map/duplicate/<int:pk>/', views.MapDuplicate.as_view(), name='map_duplicate'),
    path('map/delete/<int:pk>/', views.MapDelete.as_view(), name='map_delete'),
    path('layers', views.LayerList.as_view(), name='layer_list'),
    path('layer/create/', views.LayerCreate.as_view(), name='layer_create'),
    path('layer/<int:pk>/', views.LayerDetail.as_view(), name='layer_detail'),
    path('layer/edit/<int:pk>/', views.LayerUpdate.as_view(), name='layer_edit'),
    path('layer/delete/<int:pk>/', views.LayerDelete.as_view(), name='layer_delete'),
    path('request-account', views.RequestAccount.as_view(), name='request_account')
]
