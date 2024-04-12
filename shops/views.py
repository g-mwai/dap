from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from posts.models import *
from posts.forms import *
from .forms import *
from .models import *

from chats.models import *
from notifications.models import *
from random import sample
from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import *
from django.shortcuts import get_object_or_404 
import json
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@login_required
def new_shop(request):
    
    # post_detail = Post.objects.filter(posted_by=request.user).last()
    shop_form = NewShopForm()
    service_form = ServiceForm()
    form = LocationForm()
    context ={
     'shop_form': shop_form,
     'service_form': service_form,
   }
    return render (request, 'posts/new_shop.html', context )
