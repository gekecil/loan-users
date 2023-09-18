from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory, TextInput, Select
from django.urls import reverse
from ..models import NavLink, User, Segmentation, UserSegmentation

class UserSegmentationListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'contents/list.html'
    ordering = ['-pub_date']

    def get_queryset(self):
        queryset = super().get_queryset()

        for obj in queryset:
            obj.view_name = '%s:detail-user-segmentation' % self.request.resolver_match.app_name
            obj.full_name = obj.get_full_name()
            obj.date_updated = obj.pub_date

            obj.user_segmentation = UserSegmentation.objects.order_by('date_created').filter(user__pk=obj.pk)

            if obj.user_segmentation.exists():
                obj.date_updated = obj.user_segmentation.latest('date_updated').date_updated
                obj.user_segmentation = obj.user_segmentation.values_list('segmentation__name', flat=True)

        queryset.full_name__verbose_name = 'full name'
        queryset.user_segmentation__verbose_name = 'segmentations'
        queryset.date_updated__verbose_name = 'date updated'

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = '%s - %s' % (NavLink.objects.get(path=self.request.path).title, apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['buttons'] = [
            {'name': 'create user', 'path': reverse('%s:create-user' % self.request.resolver_match.app_name, kwargs={'slug': self.request.resolver_match.url_name})},
        ]

        context['fields'] = ['email', 'full_name', 'user_segmentation', 'auth_user', 'pub_date', 'date_updated']

        return context

class UserSegmentationDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'contents/detail.html'

    def get_object(self):
        obj = super().get_object()

        obj.full_name = obj.get_full_name()
        obj.date_updated = obj.pub_date
        obj.user_segmentation = UserSegmentation.objects.order_by('date_created').filter(user__pk=obj.pk)

        if obj.user_segmentation.exists():
            obj.date_updated = obj.user_segmentation.latest('date_updated').date_updated
            obj.user_segmentation = obj.user_segmentation.values_list('segmentation__name', flat=True)

        obj.full_name__verbose_name = 'full name'
        obj.user_segmentation__verbose_name = 'segmentations'
        obj.date_updated__verbose_name = 'date updated'

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Detail User Segmentation - %s' % apps.get_app_config(self.request.resolver_match.app_name).verbose_name
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['buttons'] = [
            {
                'name': 'submit segmentation',
                'url': reverse('%s:update-user-segmentation' % self.request.resolver_match.app_name, kwargs={'pk': self.get_object().pk}),
                'color': 'primary',
            },
            {
                'name': 'delete',
                'url': reverse('%s:delete-user' % self.request.resolver_match.app_name, kwargs={'slug': 'user-segmentations', 'pk': self.get_object().pk}),
                'color': 'danger',
            },
        ]

        context['fields'] = ['email', 'full_name', 'user_segmentation', 'auth_user', 'pub_date', 'date_updated']

        return context

class UserSegmentationUpdateView(LoginRequiredMixin, UpdateView):
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
            UserSegmentation,
            fields=('segmentation', ),
            extra=Segmentation.objects.count() - UserSegmentation.objects.filter(user=self.get_object()).count(),
            widgets={'segmentation': Select(attrs={'class': 'form-select'})},
            can_delete=False,
        )

        context['title'] = 'Update User Segmentation - %s' % apps.get_app_config(self.request.resolver_match.app_name).verbose_name
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['formset'] = inlineformset(instance=self.get_object())

        return context

    def form_valid(self, form):
        form.instance.email = self.get_object().email

        user_segmentation_for_delete = UserSegmentation.objects
        user_segmentation_can_delete = False

        for index in range(0, Segmentation.objects.count()):
            if self.request.POST.get('usersegmentation_set-%s-segmentation' % index):
                if self.request.POST.get('usersegmentation_set-%s-id' % index):
                    UserSegmentation.objects.filter(
                        id=self.request.POST.get('usersegmentation_set-%s-id' % index)
                    ).update(
                        auth_user=self.request.user,
                        segmentation=Segmentation.objects.get(pk=self.request.POST.get('usersegmentation_set-%s-segmentation' % index)),
                    )

                else:
                    UserSegmentation.objects.create(
                        auth_user=self.request.user,
                        user=self.get_object(),
                        segmentation=Segmentation.objects.get(pk=self.request.POST.get('usersegmentation_set-%s-segmentation' % index)),
                    )

            elif self.request.POST.get('usersegmentation_set-%s-id' % index):
                if user_segmentation_can_delete:
                    user_segmentation_for_delete = user_segmentation_for_delete | UserSegmentation.objects.filter(id=self.request.POST.get('usersegmentation_set-%s-id' % index))

                else:
                    user_segmentation_for_delete = user_segmentation_for_delete.filter(id=self.request.POST.get('usersegmentation_set-%s-id' % index))

                user_segmentation_can_delete = True

        if user_segmentation_can_delete:
            user_segmentation_for_delete.delete()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('%s:user-segmentations' % self.request.resolver_match.app_name)
