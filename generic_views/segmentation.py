from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value
from django.urls import reverse
from ..models import NavLink, Segmentation

class SegmentationListView(LoginRequiredMixin, ListView):
    model = Segmentation
    template_name = 'contents/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.annotate(view_name=Value('%s:update-segmentation' % self.request.resolver_match.app_name))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = '%s - %s' % (NavLink.objects.get(path=self.request.path).title, apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['buttons'] = [
            {'name': 'create segmentation', 'path': reverse('%s:create-segmentation' % self.request.resolver_match.app_name)},
        ]

        context['fields'] = ['name', 'auth_user', 'date_created', 'date_updated']

        return context

class SegmentationCreateView(LoginRequiredMixin, CreateView):
    model = Segmentation
    fields = ['name']
    template_name = 'contents/base-form.html'

    def get_form(self):
        form = super().get_form()

        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Create Segmentation - %s' % apps.get_app_config(self.request.resolver_match.app_name).verbose_name
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('%s:segmentations' % self.request.resolver_match.app_name)

class SegmentationUpdateView(LoginRequiredMixin, UpdateView):
    model = Segmentation
    fields = ['name']
    template_name = 'contents/base-form.html'

    def get_form(self):
        form = super().get_form()

        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Update Segmentation - %s' % apps.get_app_config(self.request.resolver_match.app_name).verbose_name
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('%s:segmentations' % self.request.resolver_match.app_name)
