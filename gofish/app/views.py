from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.exceptions import *

from models import Lake, StockingData, Fish, County

from django.template import Context, loader
from django.views.generic.base import TemplateView

import json, re

# Create your views here.

class MapView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        return context

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Params:
#   limit: just a simple limiter to the amount of lakes returned will sort by rank

# Returns:
#   JSON serialization of ordered lakes by rank, limited to limit
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
        return HttpResponse("POST requests only yo")


# Params:
#   limit: just a simple limiter to the amount of lakes
#   name: query to match lake name
#   minSize: minumum size for the lake in acres
#   maxSize: maximum size for the lake in acres
#   minAlt: minumum altitude for the lake in ft
#   maxAlt: maximum altitude for he lake in ft
#   county: a filter on the county of the lake, must be contained in County table
#   fish: a filter on the type of fish in the lake, must be contained in Fish table

# Returns:
#   JSON serialization of ordered (by rank) and filtered lakes
@csrf_exempt
def get_lakes_with_query(request):
    if request.method == 'POST':
        lakes = Lake.objects.all().order_by('-rank')
        query = dict()
        limit = 0

        # name first
        if 'name' in request.POST and request.POST['name'] != '':
            query['name__contains'] = request.POST['name']

        # county
        if 'county' in request.POST and request.POST['county'] not in ['', 'All']:
            try:
                county = County.objects.all().get(name=request.POST['county'])
            except ObjectDoesNotExist:
                return HttpResponse("Error in query: county does not match with any existing county")
            query['county'] = county

        # # fish
        # if 'fish' in request.POST and request.POST['fish'] != '':
        #     try:
        #         fish = Fish.objects.all().get(name=request.POST['fish'])
        #     except ObjectDoesNotExist:
        #         return HttpResponse("Error in query: fish does not match with any existing fish")

        # size
        if 'minSize' in request.POST and 'maxSize' in request.POST:
            try:
                lower = float(request.POST['minSize'])
                upper = float(request.POST['maxSize'])
            except ValueError:
                return HttpResponse("Error in query: size cannot be cast to a float")
            query['size__gt'] = lower
            query['size__lt'] = upper
            # query += 'size__range=(' + str(lower) + ',' + str(upper) + '),'

        # altitude
        if 'minAlt' in request.POST and 'maxAlt' in request.POST:
            try:
                lower = float(request.POST['minAlt'])
                upper = float(request.POST['maxAlt'])
            except ValueError:
                return HttpResponse("Error in query: altitude cannot be cast to a float")
            query['altitude__gt'] = lower
            query['altitude__lt'] = upper
            # query += 'altitude__range=(' + lower + ',' + upper + '),'

        # limit
        if 'limit' in request.POST:
            try:
                limit = int(request.POST['limit'])
            except ValueError:
                return HttpResponse("Error in query: limit cannot be cast to a int")

        if not any(query):
            return HttpResponse(serializers.serialize("json", lakes[:limit] if limit != 0 else lakes))
        else:
            # # because I'm totally gonna add another filter and forget to remove the ,
            # query = query.strip(',')
            # # when you know there's a better way than compiling a query string but you're lazy af so the simplest solution is a negative lookahead regex
            # # you know, after typing that out, I feel pretty stupid right about now
            # dark_magic_regex = r',(?!(?:[^(]*\([^)]*\))*[^()]*\))'
            # args = dict(q.split('=') for q in re.split(dark_magic_regex, query))
            filtered = lakes.filter(**query)
            return HttpResponse(serializers.serialize("json", filtered[:limit] if limit != 0 else filtered))
    else:
        return HttpResponse("POST requests only yo")


def get_query_defaults(request):
    if request.method == 'GET':
        defaults = dict(
            rank = 50,
            name ='Goin fishin!',
            county = 'All',
            fish = 'All',
            minSize = 0,

        )


