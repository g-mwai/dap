from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from posts.models import *
from posts.forms import *
from gigs.forms import *

from chats.models import *
from notifications.models import *
from random import sample
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm 
from accounts.models import User, Profile 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import *
from django.shortcuts import get_object_or_404 
import json
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from rest_framework import viewsets
from .serializers import PostSerializer

@login_required
def new_poll(request):
    
    # post_detail = Post.objects.filter(posted_by=request.user).last()
    form = PollForm()
    option_form = OptionForm()
    context ={
    #  'post_detail': post_detail,
     'form': form,
     'option_form': option_form,
   }
    return render (request, 'posts/poll.html', context )

@login_required
def new_yesno(request):
    if request.method == 'POST':
        form = YesNoForm()
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = YesNoForm()

    
    context ={
    'form': form,
   }
    return render (request, 'posts/yesno.html', context )

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(id=post_id)

@login_required
def new_sell(request):
    
    if request.method == 'POST':
        form = SellForm()
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = SellForm()

    
    context ={
    'form': form,
   }
    return render (request, 'posts/sell.html', context )

@login_required
def new_gig(request):
    
    if request.method == 'POST':
        form = gigForm()
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = gigForm()

    context ={
    'form': form,
   }
    return render (request, 'posts/new_gig.html', context )
