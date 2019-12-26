import random
import string
import uuid
import datetime

from django.views import View
from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Count, Q, F, Value
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

# PROJECT UTILS
from utils.generals import get_model


class RegisterView(View):
    template_name = 'web/person/register.html'
    context = dict()

    def get(self, request):
        # Logged-in user redirect to home
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, self.template_name, self.context)


class LoginView(View):
    template_name = 'web/person/login.html'
    context = dict()

    def get(self, request):
        # Logged-in user redirect to home
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, self.template_name, self.context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ValidationView(View):
    template_name = 'web/person/validation.html'
    context = dict()

    def get(self, request):
        return render(request, self.template_name, self.context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(View):
    template_name = 'web/person/dashboard.html'
    context = dict()

    def get(self, request):
        return render(request, self.template_name, self.context)
