from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse, resolve
from ..apps import LoanUsersConfig
from ..models import Segmentation, PrefixUrl

class SegmentationListView(LoginRequiredMixin, ListView):
    model = Segmentation
    template_name = 'admin-page/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = PrefixUrl.objects.get(url=self.request.path).title
        context['prefix_urls'] = PrefixUrl.objects.order_by('pub_date').all()

        context['buttons'] = [
            {'name': 'Create Segmentation', 'path': self.request.path+'/create'},
        ]

        context['columns'] = [
            {'attribute_name': 'name', 'column_name': 'Segmentation'},
            {'attribute_name': 'pub_date', 'column_name': 'Publication Date'},
        ]

        return context

class SegmentationCreateView(LoginRequiredMixin, CreateView):
    model = Segmentation
    template_name = 'admin-page/create-form.html'
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Create Segmentation'
        context['prefix_urls'] = PrefixUrl.objects.order_by('pub_date').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(LoanUsersConfig.name+':segmentations')
