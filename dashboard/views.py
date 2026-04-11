from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard.html'
    login_url = 'login'

    def get(self, request):
        age_groups = self._get_age_groups()
        sales_data = self._get_sales_data()
        
        context = {
            'age_groups': age_groups,
            'sales_data': sales_data,
        }
        return render(request, self.template_name, context)

    def _get_age_groups(self):
        return ['18-25', '25-35', '35-45', '45-55', '55+']

    def _get_sales_data(self):
        return [12, 19, 3, 5, 2]
