from django.urls import path
from . import apps
from .views.regular_views import DashboardView
from .views.segmentation_views import SegmentationListView, SegmentationCreateView
from .views.position_views import PositionListView, PositionCreateView
from .views.user_segmentation_views import UserSegmentationListView, UserSegmentationCreateView, UserSegmentationUpdateView, UserSegmentationDeleteView
from .views.user_position_views import UserPositionListView, UserPositionCreateView, UserPositionUpdateView, UserPositionDeleteView
from .views.user_views import UserCreateView

app_name = apps.LoanUsersConfig.name

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('segmentations', SegmentationListView.as_view(), name='segmentations'),
    path('segmentations/create', SegmentationCreateView.as_view(), name='create-segmentation'),
    path('positions', PositionListView.as_view(), name='positions'),
    path('positions/create', PositionCreateView.as_view(), name='create-position'),
    path('user-segmentations', UserSegmentationListView.as_view(), name='user-segmentations'),
    path('user-segmentations/create', UserSegmentationCreateView.as_view(), name='create-user-segmentation'),
    path('user-segmentations/<slug:slug>/update', UserSegmentationUpdateView.as_view(), name='update-user-segmentation'),
    path('user-segmentations/<slug:slug>/delete', UserSegmentationDeleteView.as_view(), name='delete-user-segmentation'),
    path('user-positions', UserPositionListView.as_view(), name='user-positions'),
    path('user-positions/create', UserPositionCreateView.as_view(), name='create-user-position'),
    path('user-positions/<int:id>/update', UserPositionUpdateView.as_view(), name='update-user-position'),
    path('user-positions/<slug:slug>/delete', UserPositionDeleteView.as_view(), name='delete-user-position'),
    path('<slug:slug>/create-user', UserCreateView.as_view(), name='create-user'),
]
