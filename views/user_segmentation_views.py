from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse, resolve
from ..apps import LoanUsersConfig
from ..models import User, Segmentation, UserSegmentation, PrefixUrl

class UserSegmentationListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'admin-page/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        for obj in queryset:
            obj.segmentation = UserSegmentation.objects.filter(user_id=obj.id)

        for obj_segmentation in obj.segmentation:
            obj_segmentation.segmentation_name = obj_segmentation.segmentation.name

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
            {'name': 'Submit Segmentation', 'path': self.request.path+'/create'},
        ]

        context['columns'] = [
            {'attribute_name': 'email', 'column_name': 'Email'},
            {'attribute_name': 'first_name', 'column_name': 'First Name'},
            {'attribute_name': 'last_name', 'column_name': 'Last Name'},
            {'attribute_name': 'segmentation', 'sub_attribute_name': 'segmentation_name', 'column_name': 'Segmentation'},
            {'attribute_name': 'pub_date', 'column_name': 'Publication Date'},
        ]

        return context

class UserSegmentationCreateView(LoginRequiredMixin, CreateView):
    model = UserSegmentation
    fields = ['user', 'segmentation']
    template_name = 'admin-page/many-values-create-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['app'] = resolve(self.request.path)
        context['site'] = Site.objects.get_current(self.request)
        context['title'] = 'Submit Segmentation'
        context['prefix_urls'] = PrefixUrl.objects.order_by('pub_date').all()
        context['many_values'] = 'segmentation'

        return context

    def form_valid(self, form):
        form.instance.auth_user = self.request.user

        for segmentation in filter(None, self.request.POST.getlist('segmentations')):
            UserSegmentation(
                auth_user=self.request.user,
                user=User.objects.get(id=self.request.POST['user']),
                segmentation=Segmentation.objects.get(id=segmentation),
            ).save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(LoanUsersConfig.name+':user-segmentations')

class UserSegmentationUpdateView(UpdateView):
    model = UserSegmentation
    fields = ['name']
    template_name = 'admin-page/create-form.html'

class UserSegmentationDeleteView(DeleteView):
    model = UserSegmentation

    def get_success_url(self):
        return reverse(LoanUsersConfig.name+':user-segmentations')
