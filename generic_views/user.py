from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.urls import reverse
from ..models import NavLink, User

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ['email', 'first_name', 'last_name']
    template_name = 'contents/base-form.html'

    def get_form(self):
        form = super().get_form()
        form.fields['last_name'].required = False

        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['request'] = self.request
        context['title'] = 'Create User - %s' % apps.get_app_config(self.request.resolver_match.app_name).verbose_name
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        route_segments = self.request.path.split('/')

        return str('/').join(route_segments[0:-1])

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'contents/confirm-delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['request'] = self.request
        context['title'] = 'Delete User - %s' % apps.get_app_config(self.request.resolver_match.app_name).verbose_name
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        return context

    def get_success_url(self):
        route_segments = self.request.path.split('/')

        return str('/').join(route_segments[0:-2])
