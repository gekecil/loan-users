from django.views.generic.base import RedirectView
from .base_views.dashboard import DashboardView
from .generic_views.position import PositionListView, PositionCreateView, PositionUpdateView
from .generic_views.segmentation import SegmentationListView, SegmentationCreateView, SegmentationUpdateView
from .generic_views.user import UserCreateView, UserDeleteView
from .generic_views.user_position import UserPositionListView, UserPositionDetailView, UserPositionUpdateView
from .generic_views.user_segmentation import UserSegmentationListView, UserSegmentationDetailView, UserSegmentationUpdateView

def home(request):
    app_name = request.resolver_match.app_name
    pattern_name = '%s:dashboard' % app_name

    return RedirectView.as_view(pattern_name=pattern_name)(request)

def dashboard(request):
    return DashboardView.as_view()(request)

def position(request):
    return PositionListView.as_view()(request)

def create_position(request):
    return PositionCreateView.as_view()(request)

def update_position(request, pk):
    return PositionUpdateView.as_view()(request, pk=pk)

def segmentation(request):
    return SegmentationListView.as_view()(request)

def create_segmentation(request):
    return SegmentationCreateView.as_view()(request)

def update_segmentation(request, pk):
    return SegmentationUpdateView.as_view()(request, pk=pk)

def user_position(request):
    return UserPositionListView.as_view()(request)

def detail_user_position(request, pk):
    return UserPositionDetailView.as_view()(request, pk=pk)

def update_user_position(request, pk):
    return UserPositionUpdateView.as_view()(request, pk=pk)

def user_segmentation(request):
    return UserSegmentationListView.as_view()(request)

def detail_user_segmentation(request, pk):
    return UserSegmentationDetailView.as_view()(request, pk=pk)

def update_user_segmentation(request, pk):
    return UserSegmentationUpdateView.as_view()(request, pk=pk)

def create_user(request, slug):
    return UserCreateView.as_view()(request)

def delete_user(request, slug, pk):
    return UserDeleteView.as_view()(request, pk=pk)
