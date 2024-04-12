from django.shortcuts import render
from accounts.models import User, Profile 
from posts.models import Post
from .models import *
from posts.forms import *
from gigs.forms import GigForm


def my_wallet(request):
    my_profile = Profile.objects.get(user=request.user)
    wallet = Wallet.objects.get(owner=request.user)
    random_industries = Industries.choices

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        gig_form = GigForm(request.POST, request.FILES)
        sell_form = SellForm(request.POST, request.FILES)
        project_form = ProjectForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.posted_by = request.user
            post.save()
            res = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(res)
        elif gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.posted_by = request.user
            gig.save()
            res = {'success': True, 'message': 'Gig submitted successfully.'}
            return JsonResponse(res)
        elif project_form.is_valid():
            project = project_form.save(commit=False)
            project.posted_by = request.user
            project.save()
            res = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(res)
        elif sell_form.is_valid():
            # Add debugging output to inspect the form data and attributes
            print("Sell form data:", sell_form.cleaned_data)
            print("Before setting post_type:", sell_form.instance.post_type)
            sell = sell_form.save(commit=False)
            sell.post_type = 'sell'
            sell.posted_by = request.user
            sell.save()
            print("After setting post_type:", sell_post.post_type)
            res = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(res)
        else:
            res = {'success': False, 'message': 'Form data is invalid.'}
            return JsonResponse(res)
    else:
        post_form = PostForm()
        gig_form = GigForm()
        sell_form = SellForm()
        project_form = ProjectForm()

    context = {
    'my_profile' : my_profile,
    'wallet': wallet,
    'post_form': post_form,
    'gig_form' : gig_form,
    'sell_form' : sell_form,
    'project_form' : project_form,
    'random_industries': random_industries,

    }

    return render (request, 'wallet/my_wallet.html', context )

def bet_yes(request, post_id):
    post = Post.objects.get(id=post_id)
    form = BetForm()
    context = {
    'post' : post,
    }

    return render (request, 'wallet/my_wallet.html', context )

