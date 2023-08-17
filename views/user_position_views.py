from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse, resolve
from ..apps import LoanUsersConfig
from ..models import User, Position, UserPosition, PrefixUrl

class UserPositionListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'admin-page/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        for obj in queryset:
            obj.position = UserPosition.objects.filter(user_id=obj.id)

        for obj_position in obj.position:
            obj_position.position_name = obj_position.position.name

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = PrefixUrl.objects.get(url=self.request.path).title
        context['prefix_urls'] = PrefixUrl.objects.order_by('pub_date').all()

        context['buttons'] = [
            {'name': 'Create User', 'path': self.request.path+'/create-user'},
            {'name': 'Submit Position', 'path': self.request.path+'/create'},
        ]

        context['columns'] = [
            {'attribute_name': 'email', 'column_name': 'Email', 'link': 'update'},
            {'attribute_name': 'first_name', 'column_name': 'First Name'},
            {'attribute_name': 'last_name', 'column_name': 'Last Name'},
            {'attribute_name': 'position', 'sub_attribute_name': 'position_name', 'column_name': 'Position'},
            {'attribute_name': 'pub_date', 'column_name': 'Publication Date'},
        ]

        return context

class UserPositionCreateView(LoginRequiredMixin, CreateView):
    model = UserPosition
    fields = ['user', 'position']
    template_name = 'admin-page/many-values-create-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Submit Position'
        context['prefix_urls'] = PrefixUrl.objects.order_by('pub_date').all()
        context['many_values'] = 'position'

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        for position in filter(None, self.request.POST.getlist('positions')):
            UserPosition(
                auth_user=self.request.user,
                user=User.objects.get(id=self.request.POST['user']),
                position=Position.objects.get(id=position),
            ).save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(LoanUsersConfig.name+':user-positions')

class UserPositionUpdateView(UpdateView):
    model = User
    fields = ['email']
    template_name = 'admin-page/many-values-update-form.html'
    pk_field = 'id'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Submit Position'
        context['prefix_urls'] = PrefixUrl.objects.order_by('pub_date').all()
        context['values'] = self.get_object()
        context['fields'] = self.get_form().fields
        context['fields']['email'] = {'name': 'email', 'label': 'email', 'widget_type': 'text'}
        context['fields']['position'] = {'name': 'position', 'label': 'position', 'widget_type': 'select'}
        context['many_values'] = 'position'

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        for position in filter(None, self.request.POST.getlist('positions')):
            UserPosition(
                auth_user=self.request.user,
                user=User.objects.get(id=self.request.POST['user']),
                position=Position.objects.get(id=position),
            ).save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(LoanUsersConfig.name+':user-positions')

class UserPositionDeleteView(DeleteView):
    model = UserPosition

    def get_success_url(self):
        return reverse(LoanUsersConfig.name+':user-positions')
