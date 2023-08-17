from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse, resolve
from ..apps import LoanUsersConfig
from ..models import User, PrefixUrl

class UserCreateView(LoginRequiredMixin, CreateView):

    model = User
    fields = ['email', 'first_name', 'last_name']
    template_name = 'admin-page/create-form.html'

    def get_form(form_class=None):

        form = super().get_form(form_class=None)
        form.fields['last_name'].required = False

        return form

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Create User'
        context['prefix_urls'] = PrefixUrl.objects.order_by('pub_date').all()

        return context

    def form_valid(self, form):

        form.instance.auth_user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):

        route_segments = self.request.path.split('/')

        return str('/').join(route_segments[0:-1])
