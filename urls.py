from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('positions', views.position, name='positions'),
    path('positions/create', views.create_position, name='create-position'),
    path('positions/<int:pk>/update', views.update_position, name='update-position'),
    path('segmentations', views.segmentation, name='segmentations'),
    path('segmentations/create', views.create_segmentation, name='create-segmentation'),
    path('segmentations/<int:pk>/update', views.update_segmentation, name='update-segmentation'),
    path('user-positions', views.user_position, name='user-positions'),
    path('user-positions/<int:pk>', views.detail_user_position, name='detail-user-position'),
    path('user-positions/<int:pk>/update', views.update_user_position, name='update-user-position'),
    path('user-segmentations', views.user_segmentation, name='user-segmentations'),
    path('user-segmentations/<int:pk>', views.detail_user_segmentation, name='detail-user-segmentation'),
    path('user-segmentations/<int:pk>/update', views.update_user_segmentation, name='update-user-segmentation'),
    path('<slug:slug>/create-user', views.create_user, name='create-user'),
    path('<slug:slug>/<int:pk>/delete-user', views.delete_user, name='delete-user'),
]
