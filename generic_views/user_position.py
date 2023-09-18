from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory, TextInput, Select
from django.urls import reverse
from ..models import NavLink, User, Position, UserPosition

class UserPositionListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'contents/list.html'
    ordering = ['-pub_date']

    def get_queryset(self):
        queryset = super().get_queryset()

        for obj in queryset:
            obj.view_name = '%s:detail-user-position' % self.request.resolver_match.app_name
            obj.full_name = obj.get_full_name()
            obj.date_updated = obj.pub_date

            obj.user_position = UserPosition.objects.order_by('date_created').filter(user__pk=obj.pk)

            if obj.user_position.exists():
                obj.date_updated = obj.user_position.latest('date_updated').date_updated
                obj.user_position = obj.user_position.values_list('position__name', flat=True)

        queryset.full_name__verbose_name = 'full name'
        queryset.user_position__verbose_name = 'positions'
        queryset.date_updated__verbose_name = 'date updated'

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = '%s - %s' % (NavLink.objects.get(path=self.request.path).title, apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['buttons'] = [
            {'name': 'create user', 'path': reverse('%s:create-user' % self.request.resolver_match.app_name, kwargs={'slug': self.request.resolver_match.url_name})},
        ]

        context['fields'] = ['email', 'full_name', 'user_position', 'auth_user', 'pub_date', 'date_updated']

        return context

class UserPositionDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'contents/detail.html'

    def get_object(self):
        obj = super().get_object()

        obj.full_name = obj.get_full_name()
        obj.date_updated = obj.pub_date
        obj.user_position = UserPosition.objects.order_by('date_created').filter(user__pk=obj.pk)

        if obj.user_position.exists():
            obj.date_updated = obj.user_position.latest('date_updated').date_updated
            obj.user_position = obj.user_position.values_list('position__name', flat=True)

        obj.full_name__verbose_name = 'full name'
        obj.user_position__verbose_name = 'positions'
        obj.date_updated__verbose_name = 'date updated'

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Detail User Position - %s' % apps.get_app_config(self.request.resolver_match.app_name).verbose_name
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['buttons'] = [
            {
                'name': 'submit position',
                'url': reverse('%s:update-user-position' % self.request.resolver_match.app_name, kwargs={'pk': self.get_object().pk}),
                'color': 'primary',
            },
            {
                'name': 'delete',
                'url': reverse('%s:delete-user' % self.request.resolver_match.app_name, kwargs={'slug': 'user-positions', 'pk': self.get_object().pk}),
                'color': 'danger',
            },
        ]

        context['fields'] = ['email', 'full_name', 'user_position', 'auth_user', 'pub_date', 'date_updated']

        return context

class UserPositionUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['email']
    template_name = 'contents/inline-form.html'

    def get_form(self):
        form = super().get_form()
        form.fields['email'].widget = TextInput(attrs={'class': 'form-control', 'readonly': True})
        form.fields['email'].required = False

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        inlineformset = inlineformset_factory(
            User,
            UserPosition,
            fields=('position', ),
            extra=Position.objects.count() - UserPosition.objects.filter(user=self.get_object()).count(),
            widgets={'position': Select(attrs={'class': 'form-select'})},
            can_delete=False,
        )

        context['title'] = 'Update User Position - %s' % apps.get_app_config(self.request.resolver_match.app_name).verbose_name
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['formset'] = inlineformset(instance=self.get_object())

        return context

    def form_valid(self, form):
        form.instance.email = self.get_object().email

        user_position_for_delete = UserPosition.objects
        user_position_can_delete = False

        for index in range(0, Position.objects.count()):
            if self.request.POST.get('userposition_set-%s-position' % index):
                if self.request.POST.get('userposition_set-%s-id' % index):
                    UserPosition.objects.filter(
                        id=self.request.POST.get('userposition_set-%s-id' % index)
                    ).update(
                        auth_user=self.request.user,
                        position=Position.objects.get(pk=self.request.POST.get('userposition_set-%s-position' % index)),
                    )

                else:
                    UserPosition.objects.create(
                        auth_user=self.request.user,
                        user=self.get_object(),
                        position=Position.objects.get(pk=self.request.POST.get('userposition_set-%s-position' % index)),
                    )

            elif self.request.POST.get('userposition_set-%s-id' % index):
                if user_position_can_delete:
                    user_position_for_delete = user_position_for_delete | UserPosition.objects.filter(id=self.request.POST.get('userposition_set-%s-id' % index))

                else:
                    user_position_for_delete = user_position_for_delete.filter(id=self.request.POST.get('userposition_set-%s-id' % index))

                user_position_can_delete = True

        if user_position_can_delete:
            user_position_for_delete.delete()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('%s:user-positions' % self.request.resolver_match.app_name)
