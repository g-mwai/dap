from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from posts.models import *
from posts.forms import *
from chats.models import *
from gigs.models import *
from gigs.forms import GigForm
from notifications.models import *
from random import sample
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm 
from accounts.models import User, Profile, UserCount
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
from moderation.forms import *
from moderation.models import Report
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_date
from posts.exceptions import InsufficientFundsError

from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from allauth.socialaccount.models import SocialAccount, SocialToken

@login_required
def home(request):
    # if request.user.is_authenticated:
    my_profile = Profile.objects.get(user=request.user)
 
    alerts_c = Alert.objects.filter(receiver=request.user, is_read=False).count()
    random_industries = Industries.choices
    posts = Post.objects.filter(post_type__in=['thread', 'project'])

    gigs = Gig.objects.all()
    res = {'success': True, 'message': 'Your post has posted'}

    current_user = request.user
    following_users = current_user.profile.followers.all()
    following = current_user.profile.following.all()
    following_posts = Post.objects.filter(posted_by__id__in=following)
    following_comments = Comment.objects.filter(comment_by__id__in=following)
    all_comments = Comment.objects.all()

    # Get users the current user is not following (excluding themselves)
    # not_following_users = User.objects.exclude(id=current_user.id).exclude(id__in=following_users)
    # followed_posts = Post.objects.filter(posted_by__in=following)

    # Randomly select two users to display
    # random_users = sample(list(not_following_users), 2)

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
  # Include request.FILES here
    context = {
     
        # 'followed_posts' : followed_posts,
        'alerts_c': alerts_c,
        'random_industries': random_industries,
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'project_form' : project_form,
        'posts': posts,
        'gigs': gigs,
        'following': following,
        'my_profile': my_profile,
        'following_posts': following_posts,
        'following_comments': following_comments,
        'all_comments': all_comments,
    }
    return render(request, 'app/home.html', context)

class GoogleLoginCallbackView(OAuth2CallbackView):
    def get_authenticated_user_data(self, provider, access_token):
        # Retrieve user data from Google using the access token
        user_data = self.get_provider().get_app(self.request).get_json(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            params={'access_token': access_token}
        )

        # Extract necessary user data (e.g., email, name)
        email = user_data.get('email')
        name = user_data.get('name')

        # Create or retrieve the corresponding user in your Django application
        try:
            # Attempt to retrieve the user associated with the Google account
            social_account = SocialAccount.objects.get(provider=provider.id, uid=user_data['sub'])
            user = social_account.user
        except SocialAccount.DoesNotExist:
            # If the user does not exist, create a new user
            user = None
        
        if not user:
            # Create a new user with the retrieved email
            user = self.create_user(email, name)
            
            # Associate the Google account with the new user
            SocialAccount.objects.create(provider=provider.id, uid=user_data['sub'], user=user)

        # Log in the user
        login(self.request, user)

        # Redirect the user to the home page
        return redirect(reverse('home'))

    def create_user(self, email, name):
        # Implement your logic to create a new user
        # This could involve creating a new User object or using your custom User model
        # You may also want to send a verification email, set additional user attributes, etc.
        # Here's a simplified example:
        from django.contrib.auth.models import User
        user = User.objects.create_user(email, email=email, first_name=name)
        return user

        
def get_bookmark_status(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Determine the bookmark status based on the current user's bookmarks
    is_bookmarked = post.bookmarked_users.filter(id=request.user.id).exists()
    return JsonResponse({'is_bookmarked': is_bookmarked})

def get_comment_bookmark_status(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Determine the bookmark status based on the current user's bookmarks
    is_bookmarked = comment.bookmarked_users.filter(id=request.user.id).exists()
    return JsonResponse({'is_bookmarked': is_bookmarked})


@login_required
def upload_post(request):
    if request.method == 'POST':
        # Get form data from the request
        # topic = request.POST.get('topic')
        body = request.POST.get('body')
        post_image = request.FILES.get('post_image')
        author_profile = get_object_or_404(Profile, user=request.user)
        user = request.user
        # Check if required data is provided
        if body:
            # Create a new Post instance
            new_post = Post(
                # topic=topic,
                body=body,
                industry=author_profile.industry,
                post_image=post_image,  # This is the image field in your Post model
                posted_by=request.user  # Assuming you're using Django's built-in User model
            )
            # Calculate the cost of posting a new post
            post_cost = 8  # Adjust this value as needed

            # Check if the user has enough coins to post
            if user.wallet.balance < post_cost:
                # Raise InsufficientFundsError if the user doesn't have enough coins
                # InsufficientFundsError as e:
                response_data = {'success': False, 'message': 'You do not have sufficient coin to create this post'}
                return JsonResponse(response_data)
            new_post.save()  # This will automatically deduct coins if the post type is 'thread'
            response_data = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(response_data)
        else:
            response_data = {'success': False, 'message': 'Invalid form data.'}
            return JsonResponse(response_data)

    # Handle GET or other HTTP methods
    response_data = {'success': False, 'message': 'Invalid request method.'}
    return JsonResponse(response_data)

@login_required
def members_list(request):
    random_industries = Industries.choices
    alerts_c = Alert.objects.filter(receiver=request.user, is_read=False).count()

    my_profile = Profile.objects.get(user=request.user)
    
     # Get the current user's profile
    current_user_profile = request.user.profile
    
    # Get a list of user IDs that the current user follows
    followed_user_ids = current_user_profile.following.values_list('user_id', flat=True)
    
    # Exclude the current user and users the current user follows
    excluded_user_ids = list(followed_user_ids) + [request.user.id]
    
    # Get a random set of users that the current user doesn't follow
    members = Profile.objects.exclude(user_id__in=excluded_user_ids).order_by('?')[:9]
    
    context = {
        'my_profile': my_profile,
        'alerts_c': alerts_c,
        'random_industries': random_industries,
        'members': members,

    }

    return render (request, 'filters/members.html', context )

@login_required
def upload_project(request):
    if request.method == 'POST':
        project_cta = request.POST.get('project_cta')
        progress = request.POST.get('progress')
        headline = request.POST.get('headline')
        cta_link = request.POST.get('cta_link')
        body = request.POST.get('body')
        post_type = "project"
        user = request.user
        industry = request.POST.get('industry')
        post_image = request.FILES.get('post_image')
        if headline and project_cta and progress and cta_link  and body and industry and post_type:
            new_post = Post(
                project_cta=project_cta,
                cta_link=cta_link,
                body=body,
                progress=progress,
                headline=headline,
                post_type = post_type,
                post_image=post_image,  # This is the image field in your Post model
                posted_by=request.user  # Assuming you're using Django's built-in User model
            )
            post_cost = 5  # Adjust this value as needed

            # Check if the user has enough coins to post
            if user.wallet.balance < post_cost:
                # Raise InsufficientFundsError if the user doesn't have enough coins
                # InsufficientFundsError as e:
                response_data = {'success': False, 'message': 'You do not have sufficient coin to create this post'}
                return JsonResponse(response_data)
            new_post.save()  # This will automatically deduct coins if the post type is 'thread'
            response_data = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(response_data)
        else:
            response_data = {'success': False, 'message': 'Invalid form data.'}
            return JsonResponse(response_data)

    # Handle GET or other HTTP methods
    response_data = {'success': False, 'message': 'Invalid request method.'}
    return JsonResponse(response_data)
  

def upload_sell(request):
    if request.method == 'POST':
        # cta = request.POST.get('cta')
        # sell_type = request.POST.get('sell_type')
        user = request.user
        headline = request.POST.get('headline')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')

        body = request.POST.get('body')
        post_type = "sell"
        post_image = request.FILES.get('post_image')
        if headline  and max_price and min_price and body:
            new_post = Post(
                post_type = post_type,
                body=body,
                headline=headline,
                min_price =min_price,
                max_price = max_price,
                post_image=post_image,  # This is the image field in your Post model
                posted_by=request.user  # Assuming you're using Django's built-in User model
            )
            post_cost = 21  # Adjust this value as needed

            # Check if the user has enough coins to post
            if user.wallet.balance < post_cost:
                # Raise InsufficientFundsError if the user doesn't have enough coins
                # InsufficientFundsError as e:
                response_data = {'success': False, 'message': 'You do not have sufficient coin to create this post'}
                return JsonResponse(response_data)
            new_post.save()  # This will automatically deduct coins if the post type is 'thread'
            response_data = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(response_data)
        else:
            response_data = {'success': False, 'message': 'Invalid form data.'}
            return JsonResponse(response_data)

    # Handle GET or other HTTP methods
    response_data = {'success': False, 'message': 'Invalid request method.'}
    return JsonResponse(response_data)
         
@login_required
def report_bug(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ReportBugForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            res = {'success': True, 'message': 'Report submitted successfully.'}
            return JsonResponse(res)

    else:
        form = ReportBugForm()
        messages.error(request, 'Report Submission failed. Please check the form.')
    context = {
        'form': form,
        'profile': profile,
    }

    return render(request, 'settings/report_bug.html', context)

@login_required
def upload_gig(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        industry = request.POST.get('industry')
        user = request.user
        gig_type = request.POST.get('gig_type')
        experience = request.POST.get('experience')
        location = request.POST.get('location')
        apply_link = request.POST.get('apply_link')

        if title and industry and gig_type and experience and location and apply_link:
            new_gig = Gig(
                apply_link=apply_link,
                title=title,
                industry=industry,
                gig_type=gig_type,
                experience=experience,
                location=location,
                body=body,  
                posted_by=request.user  # Assuming you're using Django's built-in User model
            )
            post_cost = 13  # Adjust this value as needed

            # Check if the user has enough coins to post
            if user.wallet.balance < post_cost:
                # Raise InsufficientFundsError if the user doesn't have enough coins
                # InsufficientFundsError as e:
                response_data = {'success': False, 'message': 'You do not have sufficient coin to create this post'}
                return JsonResponse(response_data)
            new_gig.save()  # This will automatically deduct coins if the post type is 'thread'
            response_data = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(response_data)
        else:
            response_data = {'success': False, 'message': 'Invalid form data.'}
            return JsonResponse(response_data)

    # Handle GET or other HTTP methods
    response_data = {'success': False, 'message': 'Invalid request method.'}
    return JsonResponse(response_data)


@login_required
def upload_avatar(request):
    if request.method == 'POST' and request.FILES['avatar']:
        avatar = request.FILES['avatar']
        request.user.profile.avatar = avatar
        request.user.profile.save()
        return JsonResponse({'message': 'Avatar updated successfully'})
    return JsonResponse({'error': 'Avatar update failed'}, status=400)

@login_required
def upload_cover(request):
    if request.method == 'POST' and request.FILES['cover']:
        cover = request.FILES['cover']
        request.user.profile.cover_image = cover
        request.user.profile.save()
        return JsonResponse({'message': 'Cover Image updated successfully'})
    return JsonResponse({'error': 'Cover Image update failed'}, status=400)


@require_POST
def update_profile(request):
    if request.method == 'POST':
     
        # Update other profile information
        request.user.profile.name = request.POST.get('name', '')
        request.user.profile.location = request.POST.get('location', '')
        request.user.profile.job_title = request.POST.get('job_title', '')

        request.user.profile.bio = request.POST.get('bio', '')
        request.user.profile.ext_link = request.POST.get('ext_link', '')

        # Save the updated profile
        request.user.profile.save()

        return JsonResponse({'message': 'Profile updated successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def post_search(request):
    query = request.GET.get('q')
    random_industries = Industries.choices
    my_profile = Profile.objects.get(user=request.user)
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
    if query:
        # Search for posts
        posts_results = Post.objects.filter(body__icontains=query)
        threads = Post.objects.filter(body__icontains=query, post_type="thread")
        deals = Post.objects.filter(body__icontains=query, post_type="sell")
        projects = Post.objects.filter(body__icontains=query, post_type="project")

        # Search for gigs
        gigs_results = Gig.objects.filter(title__icontains=query)
    else:
        posts_results = []
        gigs_results = []

    context = {
        'random_industries': random_industries,
        'posts_results': posts_results,
        'gigs_results': gigs_results,
        'query': query,
        'threads': threads,
        'deals': deals,
        'projects': projects,
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'project_form' : project_form,

    }
    return render(request, 'search/search.html', context)

# @login_required
# def follow_user(request):
#     if request.method == 'POST':
#         username_to_follow = request.POST.get('username')
#         try:
#             user_to_follow = User.objects.get(username=username_to_follow)
#             request.user.profile.following.add(user_to_follow)
#             return JsonResponse({'success': True})
#         except User.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'User not found'})
#     return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def who_to_follow(request):
    current_user = request.user
    following_users = current_user.profile.followers.all()
    # Get users the current user is not following (excluding themselves)
    not_following_users = User.objects.exclude(id=current_user.id).exclude(id__in=following_users)

    # Randomly select two users to display
    random_users = sample(list(not_following_users), 2)

    context = {
        'random_users': random_users,
    }

    return render(request, 'who_to_follow.html', context)
 
@login_required
def follow_user(request, profile_username):
    if request.is_ajax():
        profile_user = Profile.objects.get(user__username=profile_username)
        current_user_profile = request.user.profile

        if current_user_profile not in profile_user.followers.all():
            profile_user.followers.add(current_user_profile)
            Alert.objects.create(
                sender=request.user,
                receiver=profile_user.user,
                alert_type='follow',
                is_read=False
            )
            response_data = {'success': True, 'action': 'follow'}
        else:
            response_data = {'success': False, 'message': 'You have unfollowed this member.'}

        return JsonResponse(response_data)

@login_required
def unfollow_user(request, profile_username):
    if request.is_ajax():
        profile_user = Profile.objects.get(user__username=profile_username)
        current_user_profile = request.user.profile

        if current_user_profile in profile_user.followers.all():
            profile_user.followers.remove(current_user_profile)
            response_data = {'success': True, 'action': 'unfollow'}
        else:
            response_data = {'success': False, 'message': 'You are now following this member.'}

        return JsonResponse(response_data)

@login_required 
def report_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        user = request.user
        # Create a new Report object
        report = Report.objects.create(post_id=post_id, content=content, user=user)

        # Fetch the reported post
        reported_post = get_object_or_404(Post, id=post_id)
        
        # Update the flagged field of the reported post to True
        reported_post.flagged = True
        reported_post.save()
        return JsonResponse({'success': True, 'message': 'You have reported this post.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required 
def report_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        content = request.POST.get('content')
        user = request.user
        # Create a new Report object
        report = ReportComment.objects.create(comment_id=comment_id, content=content, user=user)

        # Fetch the reported post
        reported_post = get_object_or_404(Comment, id=comment_id)
        
        # Update the flagged field of the reported post to True
        reported_post.flagged = True
        reported_post.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required 
def report_gig(request):
    if request.method == 'POST':
        gig_id = request.POST.get('gig_id')
        content = request.POST.get('content')
        user = request.user
        # Create a new Report object
        report = ReportGig.objects.create(gig_id=gig_id, content=content, user=user)

        # Fetch the reported post
        reported_post = get_object_or_404(Gig, id=gig_id)
        
        # Update the flagged field of the reported post to True
        reported_post.flagged = True
        reported_post.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required 
def user_count_chart(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Parse start and end dates
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    # Filter UserCount data based on date range
    user_counts = UserCount.objects.filter(date__range=[start_date, end_date])

    # Serialize data for chart
    labels = [count.date.strftime('%d-%m') for count in user_counts]
    counts = [count.count for count in user_counts]

    return JsonResponse({'labels': labels, 'counts': counts})

@login_required
def toggle_bookmark(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.bookmarked_users.all():
        post.bookmarked_users.remove(request.user)
    else:
        post.bookmarked_users.add(request.user)

    return JsonResponse({'success': True})

@login_required
def toggle_comment_bookmark(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user in comment.bookmarked_users.all():
        comment.bookmarked_users.remove(request.user)
    else:
        comment.bookmarked_users.add(request.user)

    return JsonResponse({'success': True})


@login_required
def bookmark_list(request):
    my_profile = Profile.objects.get(user=request.user)
    random_industries = Industries.choices
    bookmarked_posts = request.user.bookmarked_posts.all()
    bookmarked_comments = request.user.bookmarked_comments.all()

    threads = request.user.bookmarked_posts.filter(post_type="thread")
    deals = request.user.bookmarked_posts.filter(post_type="sell")
    projects = request.user.bookmarked_posts.filter(post_type="project")
    
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
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'project_form' : project_form,
        'my_profile' : my_profile,
        'threads': threads,
        'deals': deals,
        'projects': projects,
        'bookmarked_posts': bookmarked_posts,
        'bookmarked_comments': bookmarked_comments,
        'random_industries' : random_industries,
    }
    return render(request, 'posts/bookmark_list.html', context)

@login_required
def toggle_repost(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    try:
        repost = Repost.objects.get(post=post, reposted_by=request.user)
        repost.delete()
        is_reposted = False
    except Repost.DoesNotExist:
        Repost.objects.create(post=post, reposted_by=request.user)
        is_reposted = True

    return JsonResponse({'success': True, 'is_reposted': is_reposted})

@login_required  
def customer_search(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(first_name__icontains=query) | Q(last_name__icontains=query)

            results= UnitTenant.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'search/customer_search.html', context)

        else:
            return render(request, 'search/customer_search.html')

    else:
        return render(request, 'search/customer_search.html')
@login_required   
def upvote_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.is_authenticated:
        post.upvote(request.user)

        # Create an alert for the post owner
        if post.posted_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=post.posted_by,
                alert_type='like',
                post=post,
                is_read=False
            )

        return JsonResponse({'success': True, 'vote_count': post.vote_count})
    return JsonResponse({'success': False})

@login_required
def upvote_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user.is_authenticated:
        comment.upvote(request.user)

        # Create an alert for the comment owner
        if comment.comment_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=comment.comment_by,
                alert_type='like',
                comment=comment,
                is_read=False
            )

        return JsonResponse({'success': True, 'vote_count': comment.vote_count})
    return JsonResponse({'success': False})

@login_required
def upvote_reply(request, reply_id):
    reply = Reply.objects.get(pk=reply_id)
    if request.user.is_authenticated:
        reply.upvote(request.user)

        # Create an alert for the reply owner
        if reply.reply_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=reply.reply_by,
                alert_type='like',
                reply=reply,
                is_read=False
            )

        return JsonResponse({'success': True, 'vote_count': reply.vote_count})
    return JsonResponse({'success': False})



# @login_required
# def private_chat_view(request, other_user_id):
#     other_user = get_object_or_404(User, id=other_user_id)
#     # Create or retrieve a chat room between the current user and the other user
#     chat_room, created = ChatRoom.objects.get_or_create(user1=request.user, user2=other_user)
#     return render(request, 'private_chat_room.html', {'chat_room': chat_room})


def downvote_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.is_authenticated:
        post.downvote(request.user)
        return JsonResponse({'success': True, 'vote_count': post.vote_count})
    return JsonResponse({'success': False})
  

def downvote_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user.is_authenticated:
        comment.downvote(request.user)
        return JsonResponse({'success': True, 'vote_count': comment.vote_count})
    return JsonResponse({'success': False})
  

def downvote_reply(request, reply_id):
    reply = Reply.objects.get(pk=reply_id)
    if request.user.is_authenticated:
        reply.downvote(request.user)
        return JsonResponse({'success': True, 'vote_count': reply.vote_count})
    return JsonResponse({'success': False})
  

def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile_to_follow = user_to_follow.profile
    user_profile = request.user.profile

    if user_profile != profile_to_follow:
        if user_profile.following.filter(id=profile_to_follow.id).exists():
            user_profile.following.remove(profile_to_follow)
            followed = False
        else:
            user_profile.following.add(profile_to_follow)
            followed = True
            Alert.objects.create(
                sender=request.user,
                receiver=user_profile.user,
                alert_type='follow',
                is_read=False
            )
        return JsonResponse({'followed': followed})
    else:
        return JsonResponse({'error': 'You cannot follow yourself'})


@login_required  
def follow_list(request, profile_username):
    user_id = get_user_model().objects.get(username=profile_username)

    profile_user = Profile.objects.get(user=user_id)
    # followers = Profile.objects.filter(fol)
    profile = Profile.objects.get(user=user_id)

    following = profile_user.following.all()
    followers = profile_user.followers.all()

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
        
    context ={
     'following': following,
     'followers': followers,
     'profile_user': profile_user,
     'profile': profile,
     'post_form': post_form,
     'gig_form' : gig_form,
     'sell_form' : sell_form,
     'project_form' : project_form,
     
    }
    
    return render (request, 'profiles/following_list.html', context )

@login_required
def edit_account(request):
    # Check if the password has been confirmed
    # if not request.session.get('password_confirmed'):
    #     messages.warning(request, 'Please confirm your password to edit your account.')
    #     return redirect('confirm_password')  # Redirect to password confirmation view

    profile = request.user.profile
    random_industries = Industries.choices
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=profile)
        if form.is_valid():

            form.save()
            messages.success(request, 'Your profile has been updated successfully')


            return redirect(settings)  
    else:
        form = EditAccountForm(instance=profile)
        messages.error(request, 'Profile update failed. Please check the form.')
    context = {
        'form': form,
        'random_industries': random_industries,
    }

    return render(request, 'profiles/edit_account.html', context)


def toggle_pin(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Toggle the pin status of the post
    post.is_pinned = not post.is_pinned
    post.save()
    
    return JsonResponse({'success': True})


def edit_username(request):
    # # Check if the password has been confirmed
    # if not request.session.get('password_confirmed'):
    #     messages.warning(request, 'Please confirm your password to edit your account.')
    #     return redirect('confirm_username')

    if request.method == 'POST':
        form = EditUsernameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
        
        # Check if the new username is available
            if User.objects.filter(username=new_username).exists():
                response_data = {'message': 'Username is already taken.'}
            else:
            # Update the user's username
                request.user.username = new_username
                request.user.save()
            
            # Update the associated profile's username
                request.user.profile.user = request.user
                request.user.profile.save()
            
                response_data = {'message': 'Username updated successfully.'}
        else:
            response_data = {'message': 'Invalid form data.'}

        return JsonResponse(response_data)
    else:
        form = EditUsernameForm()

    context = {
        'form': form,
    }

    return render(request, 'settings/username.html', context)

# @login_required
def view_profile(request, profile_username):
    res = {'success': True, 'message': 'Your post has posted'}

    # Get the user object based on the provided username
    profile_user = get_user_model().objects.get(username=profile_username)
    
    # Check if the user has a corresponding profile
    profile_detail, created = Profile.objects.get_or_create(user=profile_user)
    
    # Fetch other profile details and posts related to the user
    profile_posts = Post.objects.filter(posted_by=profile_user)
    post_comments = Comment.objects.filter(comment_by=profile_user)
    pinned_post = Post.objects.filter(posted_by=profile_user, is_pinned=True)
    pinned_c = Post.objects.filter(posted_by=profile_user, is_pinned=True).count()
    posts_count = profile_posts.count()
    if request.user.is_authenticated:
        my_profile = Profile.objects.get(user=request.user)

        # Fetch the logged-in user's profile
        profile = request.user.profile
    
        # Check if the logged-in user follows the profile_user
        follows = profile.following.filter(user=profile_user).exists()
    posts_c = Post.objects.filter(posted_by=profile_user).count()
    threads = Post.objects.filter(post_type="thread", posted_by=profile_user)
    deals = Post.objects.filter(post_type="sell", posted_by=profile_user)
    projects = Post.objects.filter(post_type="project", posted_by=profile_user)

    # Check if the profile_user follows the logged-in user
    if request.user.is_authenticated:
        followed_by = profile_user.profile.following.filter(user=request.user).exists()
    random_industries = Industries.choices
    # Process the form submission if it's a POST request
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST, request.FILES, instance=profile_detail)
        form = LoginForm(request, data=request.POST)
        post_form = PostForm(request.POST, request.FILES)
        gig_form = GigForm(request.POST, request.FILES)
        sell_form = SellForm(request.POST, request.FILES)
        project_form = ProjectForm(request.POST, request.FILES)

        if edit_profile_form.is_valid():
            edit_profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
    
            return redirect(request.META['HTTP_REFERER'])

        elif post_form.is_valid():
            post = post_form.save(commit=False)
            post.posted_by = request.user
            post.save()
            res = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(res)
        elif project_form.is_valid():
            project = project_form.save(commit=False)
            project.posted_by = request.user
            project.save()
            res = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(res)
        elif gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.posted_by = request.user
            gig.save()
            res = {'success': True, 'message': 'Gig submitted successfully.'}
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
        elif form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome, you are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        
    else:
        post_form = PostForm()
        gig_form = GigForm()
        form = LoginForm()
        sell_form = SellForm()
        project_form = ProjectForm()
        edit_profile_form = EditProfileForm(instance=profile_detail)
        messages.error(request, 'Profile update failed. Please check the form.')
    if request.user.is_authenticated:
        context = {
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'posts_c': posts_c,
        'project_form': project_form,
        'profile_user': profile_user,
        'profile_detail': profile_detail,
        'profile_posts': profile_posts,
        'posts_count': posts_count,
        'profile': profile,
        'my_profile': my_profile,
        'edit_profile_form': edit_profile_form,
        'follows': follows,
        'threads': threads,
        'deals': deals,
        'projects': projects,
        'followed_by': followed_by,
        'random_industries': random_industries,
        'post_comments': post_comments,
        'pinned_post': pinned_post,
        'pinned_c': pinned_c,
        }
    else:
        context = {
        'threads': threads,
        'deals': deals,
        'projects': projects,
        'random_industries': random_industries,
        'posts_c': posts_c,
        'profile_detail': profile_detail,
        'profile_posts': profile_posts,
        "login_form": form,
        'post_comments': post_comments,
        }


    
    return render(request, 'profiles/userprofile.html', context)


def view_shop(request, profile_username):
    res = {'success': True, 'message': 'Your post has posted'}

    # Get the user object based on the provided username
    profile_user = get_user_model().objects.get(username=profile_username)
    
    # Check if the user has a corresponding profile
    profile_detail, created = Profile.objects.get_or_create(user=profile_user)
    
    # Fetch other profile details and posts related to the user
    profile_posts = Post.objects.filter(posted_by=profile_user)
    posts_count = profile_posts.count()
    if request.user.is_authenticated:
        my_profile = Profile.objects.get(user=request.user)

        # Fetch the logged-in user's profile
        profile = request.user.profile
    
        # Check if the logged-in user follows the profile_user
        follows = profile.following.filter(user=profile_user).exists()
    projects_c = Post.objects.filter(post_type="project", posted_by=profile_user).count()
    threads = Post.objects.filter(post_type="thread", posted_by=profile_user)
    deals = Post.objects.filter(post_type="sell", posted_by=profile_user)
    projects = Post.objects.filter(post_type="project", posted_by=profile_user)

    # Check if the profile_user follows the logged-in user
    if request.user.is_authenticated:
        followed_by = profile_user.profile.following.filter(user=request.user).exists()
    random_industries = Industries.choices
    # Process the form submission if it's a POST request
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST, request.FILES, instance=profile_detail)
        form = LoginForm(request, data=request.POST)
        post_form = PostForm(request.POST, request.FILES)
        gig_form = GigForm(request.POST, request.FILES)
        sell_form = SellForm(request.POST, request.FILES)
        project_form = ProjectForm(request.POST, request.FILES)

        if edit_profile_form.is_valid():
            edit_profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
    
            return redirect(request.META['HTTP_REFERER'])

        elif post_form.is_valid():
            post = post_form.save(commit=False)
            post.posted_by = request.user
            post.save()
            res = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(res)
        elif project_form.is_valid():
            project = project_form.save(commit=False)
            project.posted_by = request.user
            project.save()
            res = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(res)
        elif gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.posted_by = request.user
            gig.save()
            res = {'success': True, 'message': 'Gig submitted successfully.'}
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
        elif form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome, you are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        
    else:
        post_form = PostForm()
        gig_form = GigForm()
        form = LoginForm()
        sell_form = SellForm()
        project_form = ProjectForm()
        edit_profile_form = EditProfileForm(instance=profile_detail)
        messages.error(request, 'Profile update failed. Please check the form.')
    if request.user.is_authenticated:
        context = {
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'projects_c': projects_c,
        'project_form': project_form,
        'profile_user': profile_user,
        'profile_detail': profile_detail,
        'profile_posts': profile_posts,
        'posts_count': posts_count,
        'profile': profile,
        'my_profile': my_profile,
        'edit_profile_form': edit_profile_form,
        'follows': follows,
        'threads': threads,
        'deals': deals,
        'projects': projects,
        'followed_by': followed_by,
        'random_industries': random_industries,
        }
    else:
        context = {
        'threads': threads,
        'deals': deals,
        'projects': projects,
        'random_industries': random_industries,
        'projects_c': projects_c,
        'profile_detail': profile_detail,
        'profile_posts': profile_posts,
        "login_form": form,
        
        }


    
    return render(request, 'profiles/userprofile.html', context)

@require_POST
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_text = request.POST.get('comment')
    comment_image = request.FILES.get('comment_image')

    if comment_text:
        comment = Comment.objects.create(
            comment_by=request.user,
            parent_post=post,
            body=comment_text,
            comment_image=comment_image
        )
        post.comment_count += 1
        post.save()

        # Create an alert for the post owner
        if post.posted_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=post.posted_by,
                alert_type='comment',
                post=post,
                is_read=False
            )

        return JsonResponse({'message': 'Comment added successfully'})
    else:
        return JsonResponse({'error': 'Comment text is required'}, status=400)
    
@require_POST
def add_reply(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    reply_text = request.POST.get('reply')

    if reply_text:
        reply = Reply.objects.create(
            reply_by=request.user,
            related_comment=comment,
            body=reply_text
        )
        comment.reply_count += 1
        comment.save()

        # Create an alert for the post owner
        if reply.reply_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=reply.reply_by,
                alert_type='reply',
                reply=reply,
                is_read=False
            )

        return JsonResponse({'message': 'reply added successfully'})
    else:
        return JsonResponse({'error': 'reply text is required'}, status=400)
    
       
def get_comment_count(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_count = Comment.objects.filter(parent_post=post).count()
    return JsonResponse({'comment_count': comment_count})

def get_reply_count(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    reply_count = Reply.objects.filter(related_comment=comment).count()
    return JsonResponse({'reply_count': reply_count})

def check_unread_alerts(request):
    if request.user.is_authenticated:
        unread_alerts_count = Alert.objects.filter(receiver=request.user, is_read=False).count()
        return JsonResponse({'unread_alerts_count': unread_alerts_count})
    else:
        return JsonResponse({'unread_alerts_count': 0})

def mark_alerts_as_read(request):
    if request.user.is_authenticated:
        Alert.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})

@login_required
def post_detail(request, identifier):
    my_profile = Profile.objects.get(user=request.user)
    post_detail = get_object_or_404(Post, identifier=identifier)
    post_comments = Comment.objects.filter(parent_post=post_detail)
    comment_counter = post_comments.count()
    random_industries = Industries.choices
     # Check if the user has already viewed this post
    if not View.objects.filter(post=post_detail, viewer=request.user).exists():
        # If not, create a new view record
        View.objects.create(post=post_detail, viewer=request.user)
    
    for comment in post_comments:
        comment.replies = Reply.objects.filter(related_comment=comment)

    if request.method == 'POST':
        post_comment_form = NewCommentForm(request.POST)
    
        if post_comment_form.is_valid():
            post_comment_form.instance.comment_by = request.user
            post_comment_form.instance.parent_post = post_detail
            post_comment_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect(request.META['HTTP_REFERER'])
        elif post_form.is_valid():
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
        new_comment_form = NewCommentForm(request.POST)
        post_form = PostForm()
        gig_form = GigForm()
        sell_form = SellForm()
        project_form = ProjectForm()

    context ={
     'post_form': post_form,
     'gig_form' : gig_form,
     'sell_form' : sell_form,
     'project_form' : project_form,
     'my_profile': my_profile,
     'post_detail': post_detail,
     'post_comments':post_comments,
     'new_comment_form': new_comment_form,
     'comment_counter':comment_counter,
     'random_industries' : random_industries
   }
    # view_post(request, id)

    return render (request, 'posts/post_detail.html', context )


# @login_required
def market(request):
    if request.user.is_authenticated:
        my_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(post_type='sell')
    
    # Get users that the current user follows
    if request.user.is_authenticated:
        following_users = my_profile.following.all().values_list('user', flat=True)
    
        # Exclude users that the current user already follows
        members = Profile.objects.exclude(user__in=following_users)[:12]
    
    random_industries = Industries.choices
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        gig_form = GigForm(request.POST, request.FILES)
        sell_form = SellForm(request.POST, request.FILES)
        project_form = ProjectForm(request.POST, request.FILES)
        form = LoginForm(request, data=request.POST)
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
        elif form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome, you are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            res = {'success': False, 'message': 'Form data is invalid.'}
            return JsonResponse(res)
    else:
        post_form = PostForm()
        gig_form = GigForm()
        form = LoginForm()
        sell_form = SellForm()
        project_form = ProjectForm()
    if request.user.is_authenticated:
        context ={
        'my_profile': my_profile,
        'posts': posts,
        'members': members,
        'random_industries': random_industries,
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'project_form' : project_form,
        }
    else:
        context ={
        'posts': posts,
        'random_industries': random_industries,
        "login_form": form,
        }
        
    return render(request, 'markets/shop.html', context)


def policy(request, policy):
    user = request.user
    # my_profile = Profile.objects.get(user=user)
    random_industries = Industries.choices
    policy = Policy.objects.get(pol=policy)
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome, you are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            res = {'success': False, 'message': 'Form data is invalid.'}
            return JsonResponse(res)
    else:
        form = LoginForm()
    context ={
        'policy': policy,
        # 'my_profile': my_profile
        'random_industries': random_industries,
        "login_form": form,
        }
    return render(request, 'policies/policy.html', context)

@login_required
def industry_filter(request, industry):
    user = request.user
    my_profile = Profile.objects.get(user=user)
    filtered_posts = Post.objects.filter(industry=industry)
    threads = Post.objects.filter(post_type="thread", industry=industry)
    projects = Post.objects.filter(post_type="project", industry=industry)
    filtered_gigs = Gig.objects.filter(industry=industry)

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

    context ={
        'filtered_posts': filtered_posts,
        'filtered_gigs': filtered_gigs,
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'project_form' : project_form,
        'industry': industry,
        'threads': threads,
        'projects': projects,
        'my_profile': my_profile,
        'random_industries': random_industries
        }
    return render(request, 'filters/industry_posts.html', context)

@login_required
def industry_list(request):
    user = request.user
    my_profile = Profile.objects.get(user=user)
    industries = Industries.choices

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

    context ={
        'industries': industries,
        'my_profile': my_profile,
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'project_form' : project_form,

        }
    return render(request, 'filters/industry_list.html', context)


def xp_filter(request, experience):
    user = request.user
    my_profile = Profile.objects.get(user=user)
    filtered_gigs = Gig.objects.filter(experience=experience)
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

    context ={
        'filtered_gigs': filtered_gigs,
        'experience': experience,
        'my_profile': my_profile,
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'project_form' : project_form,
        'random_industries': random_industries
        }
    return render(request, 'filters/xp_filter.html', context)


def type_filter(request, gig_type):
    user = request.user
    my_profile = Profile.objects.get(user=user)
    filtered_gigs = Gig.objects.filter(gig_type=gig_type)
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

    context ={
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'project_form' : project_form,
        'filtered_gigs': filtered_gigs,
        'gig_type': gig_type,
        'my_profile': my_profile,
        'random_industries': random_industries
        }
    return render(request, 'filters/type_filter.html', context)


@login_required
def chat_list(request):
       
    context ={
     
   }
    return render (request, 'chats/chatlist.html', context )

def explore(request):
    my_profile = Profile.objects.get(user=request.user)

    posts =  Post.objects.all() 
    context ={
     'my_profile' : my_profile,
     'posts': posts,
   }
    return render (request, 'search/explore.html', context )


# @login_required
# def notification_list(request):
       
#     context ={
     
#    }
#     return render (request, 'notifications/notificationlist.html', context )

@login_required
def settings(request):
    profile = request.user.profile
    profile_detail = Profile.objects.get(user=request.user)
    random_industries = Industries.choices
    my_profile = Profile.objects.get(user=request.user)

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
        # 'form': form,
        'random_industries': random_industries,
        'profile': profile,
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'my_profile': my_profile,
        'project_form' : project_form,
    }
    return render (request, 'settings/user_settings.html', context )

# @login_required
# @require_POST
# def edit_profile_dyna(request):
#     if request.method == 'POST':
#         form = EditAccountForm(request.POST, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True})
#         else:
#             errors = form.errors.as_json()
#             return JsonResponse({'success': False, 'errors': errors})
#     else:
#         form = EditAccountForm(instance=request.user.profile)

#     return render(request, 'profiles/edit_profile.html', {'form': form})

def get_like_dislike_data(request, post_id):
    post = Post.objects.get(pk=post_id)
    
    like_count = post.likes.count()
    dislike_count = post.dislikes.count()

    data = {
        'like_count': like_count,
        'dislike_count': dislike_count,
    }

    return JsonResponse(data)
    

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    my_profile = Profile.objects.get(user=request.user)
    random_industries = Industries.choices

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=profile)
        if form.is_valid():
            
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = EditAccountForm(instance=profile)

    context = {
    'form': form,
    'my_profile': my_profile,
    'random_industries': random_industries,
    }
    return render(request, 'profiles/edit_profile.html', context)

@login_required
def view_alerts(request):
    # Retrieve unread alerts for the logged-in user
    user_alerts = Alert.objects.filter(receiver=request.user, is_read=False)
    my_profile = Profile.objects.get(user=request.user)
    random_industries = Industries.choices
    # Mark retrieved alerts as read
    # user_alerts.update(is_read=True)

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
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'project_form' : project_form,
        'user_alerts': user_alerts,
        'my_profile' : my_profile,
        'random_industries' : random_industries,
        }
    return render(request, 'notifications/notificationlist.html', context)

def booking(request):
    my_profile = Profile.objects.get(user=request.user)
    random_industries = Industries.choices
    # Mark retrieved alerts as read
    # user_alerts.update(is_read=True)

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
        'random_industries': random_industries,
        'post_form': post_form,
        'gig_form' : gig_form,
        'sell_form' : sell_form,
        'my_profile': my_profile,
        'project_form' : project_form,
    }

    return render (request, 'bookings/bookings.html', context )


def landing(request):
    posts = Post.objects.all()

    form = LoginForm(request, data=request.POST)
    signup_form = NewUserForm(request.POST)
    if request.method == "POST":
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect(edit_profile)
        messages.error(request, "Unsuccessful registration. Invalid information.")

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome, you are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = LoginForm()
    signup_form = NewUserForm()
    context ={
        "login_form": form,
        "signup_form": signup_form,
        "posts": posts,
    }
    return render (request, 'shop/shop.html', context )


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.user == post.posted_by:
        post.delete()
        return JsonResponse({'message': 'Post deleted successfully'})
    else:
        return JsonResponse({'error': 'Unauthorized to delete this post'}, status=403)


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.user == comment.comment_by:
        comment.delete()
        return JsonResponse({'message': 'Comment deleted successfully'})
    else:
        return JsonResponse({'error': 'Unauthorized to delete this comment'}, status=403)


def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    
    if request.user == reply.reply_by:
        reply.delete()
        return JsonResponse({'message': 'Reply deleted successfully'})
    else:
        return JsonResponse({'error': 'Unauthorized to delete this reply'}, status=403)

def delete_gig(request, gig_id):
    gig = get_object_or_404(Gig, pk=gig_id)
    
    if request.user == gig.posted_by:
        gig.delete()
        return JsonResponse({'message': 'Gig deleted successfully'})
    else:
        return JsonResponse({'error': 'Unauthorized to delete this gig'}, status=403)


def delete_avatar(request):
    if request.method == 'POST':
        # Delete the user's current avatar (you may need to adapt this logic)
        request.user.profile.avatar.delete()
        return JsonResponse({'message': 'Avatar deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def delete_cover(request):
    if request.method == 'POST':
        # Delete the user's current avatar (you may need to adapt this logic)
        request.user.profile.cover_image.delete()
        return JsonResponse({'message': 'Cover image deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

# @login_required
# def confirm_password(request):
#     form = ConfirmPassword()

#     if request.method == 'POST':
#         password = request.POST['password']
#         user = authenticate(username=request.user.username, password=password)

#         if user is not None:
#             # Password is correct, store a flag in the session
#             request.session['password_confirmed'] = True
#             return redirect('edit_account')  # Replace with your edit account URL
#         else:
#             messages.error(request, 'Incorrect password. Please try again.')
#     context = {
#         'form': form,
#     }
#     return render(request, 'auth/confirm_account.html', context)

   
# @login_required
# def confirm_username(request):
#     form = ConfirmPassword()

#     if request.method == 'POST':
#         password = request.POST['password']
#         user = authenticate(username=request.user.username, password=password)

#         if user is not None:
#             # Password is correct, store a flag in the session
#             request.session['password_confirmed'] = True
#             return redirect('edit_username')  # Replace with your edit account URL
#         else:
#             messages.error(request, 'Incorrect password. Please try again.')
#     context = {
#         'form': form,
#     }
#     return render(request, 'auth/confirm_account.html', context)

def fofo(request):
    context = {

    }
    return render (request, 'secondary/404.html', context )


def dashboard(request):
    context = {

    }

    return render (request, 'dashboard/dashboard.html', context )

def manifesto(request):
    context = {

    }

    return render (request, 'secondary/manifesto.html', context )
