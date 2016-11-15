from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from django.template import Context, loader
from django.views.generic.base import TemplateView

# Create your views here.

class MapView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        return context

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")