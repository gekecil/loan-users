from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse, resolve
from ..models import PrefixUrl, User, UserSegmentation, UserPosition

class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'admin-page/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = PrefixUrl.objects.get(url=self.request.path).title
        context['prefix_urls'] = PrefixUrl.objects.order_by('pub_date').all()
        context['users'] = User.objects
        context['segmentations'] = UserSegmentation.objects.distinct('user_id')
        context['positions'] = UserPosition.objects.distinct('user_id')

        return context
