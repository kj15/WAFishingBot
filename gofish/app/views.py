from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from models import Lake, StockingData, Fish, County

from django.template import Context, loader
from django.views.generic.base import TemplateView

import json

# Create your views here.

class MapView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        return context

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Params:
# limit: just a simple limiter to the amount of lakes returned will sort by rank

# Returns:
# JSON serialization of ordered lakes by rank, limited to limit
@csrf_exempt
def get_lakes_all(request):
    if request.method == 'POST':
        lakes = Lake.objects.all().order_by('-rank')
        if 'limit' in request.POST:
            if request.POST['limit'].isdigit():
                limit = int(request.POST['limit'])
                return HttpResponse(serializers.serialize("json", lakes[:limit]))
            else:
                return HttpResponse("Improperly formatted query parameter: limit")
        else:
            return HttpResponse(serializers.serialize("json", lakes))
    else:
        return HttpResponse("POST methods only yo")

def get_lakes_with_query(request):
    pass