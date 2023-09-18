import datetime
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.core.exceptions import FieldError
from ..models import NavLink, User, UserSegmentation, UserPosition

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'contents/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        chart_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des']
        models = [User, UserPosition, UserSegmentation]
        now = datetime.datetime.now()

        line_chart = {
            'datasets': []
        }

        for model in models:
            model_index = models.index(model)

            line_chart['datasets'].append({'label': model._meta.verbose_name.title()})

            for chart_label in chart_labels[0:now.month]:
                queryset = model.objects

                try:
                    queryset = queryset.filter(pub_date__year=now.year, pub_date__month=chart_labels.index(chart_label)+1)

                except FieldError:
                    queryset = queryset.filter(date_created__year=now.year, date_created__month=chart_labels.index(chart_label)+1)

                if 'data' not in line_chart['datasets'][model_index]:
                    line_chart['datasets'][model_index]['data'] = {
                        chart_label: queryset.count()
                    }

                else:
                    line_chart['datasets'][model_index]['data'][chart_label] = queryset.count()

        context['title'] = '%s - %s' % (NavLink.objects.get(path=self.request.path).title, apps.get_app_config(self.request.resolver_match.app_name).verbose_name)
        context['nav_links'] = NavLink.objects.order_by('date_created').all()

        context['line_chart'] = line_chart

        return context
