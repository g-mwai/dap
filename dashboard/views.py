from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.models import *
from posts.models import *
from moderation.models import *
from django.utils import timezone
from datetime import timedelta
from posts.forms import NewArticleForm, NewTagForm
from wallet.models import Wallet
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404 
from django.contrib import messages
from notifications.models import Alert
from moderation.forms import *
from django.db import transaction
from .decorators import superuser_required  # Import the custom decorator
from shops.models import *
from posts.forms import ProductForm, TagForm

@superuser_required
def dashboard(request):
    # Retrieve the current user's profile
    my_profile = Profile.objects.get(user=request.user)
    categories = Categories.choices  
    # Count the number of profiles, posts, and reports
    members_c = Profile.objects.count()
    posts_c = Post.objects.count()
    pr = Report.objects.count() 
    cr = ReportComment.objects.count()
    br = ReportBug.objects.count()
    gr = ReportGig.objects.count()
    reports_c = pr + cr + br + gr 
    
    # Define a function to calculate total earnings
    def calculate_total_earnings():
        # Retrieve all Wallet objects and sum up the total_earn attribute
        total_earnings = Wallet.objects.aggregate(total_earnings=Sum('total_earn'))['total_earnings']
        # If total_earnings is None (i.e., no Wallet objects exist), set it to 0
        if total_earnings is None:
            total_earnings = 0
        return total_earnings
    
    # Calculate total earnings
    total_earnings = calculate_total_earnings()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        tag_form = TagForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.post_type = 'product'
            product.posted_by = request.user
            product.save()
            print("After setting post_type:", sell_post.post_type)
            res = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(res)
        elif tag_form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            res = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(res)
    else:
        form = ProductForm()
        tag_form = TagForm()
    context = {
        'my_profile': my_profile,
        'members_c': members_c,
        'posts_c': posts_c,
        'reports_c': reports_c,
        'total_earnings': total_earnings,
        'categories': categories,
        'form': form,
        'tag_form': tag_form,
    }

    return render(request, 'dashboard/dashboard.html', context)

@superuser_required
def user_count_chart(request):
    # Get the current date and the date 24 hours ago
    today = timezone.now().date()
    twenty_four_hours_ago = today - timedelta(days=1)

    # Fetch UserCount data for the last 24 hours
    user_counts = UserCount.objects.filter(date__gte=twenty_four_hours_ago, date__lte=today).order_by('date')

    # Extract the dates and user counts from the queryset
    dates = [uc.date.strftime('%Y-%m-%d') for uc in user_counts]
    counts = [uc.count for uc in user_counts]

    # Prepare data to send to the client side
    data = {
        'dates': dates,
        'counts': counts,
    }

    return JsonResponse(data)

@superuser_required
def reported_post(request, id):
    my_profile = Profile.objects.get(user=request.user)

    post_detail = Post.objects.get(id=id)
    post_reports = Report.objects.filter(post=post_detail)
   
    context ={
     'my_profile': my_profile,
     'post_detail': post_detail,
     'post_reports': post_reports,

   }

    return render (request, 'dashboard/reported_post.html', context )

@superuser_required
def reported_comment(request, id):
    my_profile = Profile.objects.get(user=request.user)

    comment = Comment.objects.get(id=id)
    post_reports = ReportComment.objects.filter(comment=comment)
   
    context ={
     'my_profile': my_profile,
     'comment': comment,
     'post_reports': post_reports,

   }

    return render (request, 'dashboard/reported_comment.html', context )


@superuser_required
def reported_gig(request, id):
    my_profile = Profile.objects.get(user=request.user)

    gig = Gig.objects.get(id=id)
    post_reports = ReportGig.objects.filter(gig=gig)
   
    context ={
     'my_profile': my_profile,
     'gig': gig,
     'post_reports': post_reports,

   }

    return render (request, 'dashboard/reported_gig.html', context )


@superuser_required
def reported_bug(request, id):
    my_profile = Profile.objects.get(user=request.user)

    bug = ReportBug.objects.get(id=id)
    if request.method == 'POST':
        form = ReportBugForm(request.POST, instance=bug)
        if form.is_valid():

            form.save()
            messages.success(request, 'Your bug report has been updated successfully')

            return redirect('reports')
    else:
        form = ReportBugForm(instance=bug)
        messages.error(request, 'Report update failed. Please check the form.')
    context ={
     'my_profile': my_profile,
     'bug': bug,
     'form': form,

   }

    return render (request, 'dashboard/reported_bug.html', context )

@superuser_required
def members(request):
    members = Profile.objects.all()

    context = {
    'members' : members,
    }

    return render (request, 'dashboard/member_list.html', context )

def posts(request):
    posts = Post.objects.all()

    context = {
    'posts' : posts,
    }

    return render (request, 'dashboard/member_list.html', context )

@superuser_required
def docs(request):
    docs = Policy.objects.all()

    context = {
    'docs' : docs,
    }

    return render (request, 'dashboard/docs_list.html', context )

@superuser_required
def new_doc(request):
    if request.method == 'POST':
        form = NewPolicyForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, 'Your document has been updated successfully')

            return redirect('docs')
    else:
        form = NewPolicyForm()
        messages.error(request, 'Report update failed. Please check the form.')
    context = {
    'form' : form,
    
    }

    return render (request, 'dashboard/new_doc.html', context )


@superuser_required
def doc_detail(request, id):
    doc = Policy.objects.get(id=id)
    if request.method == 'POST':
        form = NewPolicyForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your document has been updated successfully')

            return redirect('docs')
    else:
        form = NewPolicyForm(instance=doc)
        messages.error(request, 'Report update failed. Please check the form.')
    
    context = {
    'doc' : doc,
    'form': form,
    }

    return render (request, 'dashboard/doc_detail.html', context )


@superuser_required
def earnings(request):
    wallets = Wallet.objects.all()

    context = {
    'wallets' : wallets,
    }

    return render (request, 'dashboard/earnings.html', context )

@superuser_required
def earnings(request):
    wallets = Wallet.objects.all()

    context = {
    'wallets' : wallets,
    }

    return render (request, 'dashboard/earnings.html', context )


@superuser_required
def reports(request):
    bugs = ReportBug.objects.all()
    comments = Comment.objects.filter(flagged=True)
    gigs = Gig.objects.filter(flagged=True)
    reported_posts = Post.objects.filter(flagged=True)

    # Paginate the reported posts
    post_paginator = Paginator(reported_posts, 10)
    post_page_number = request.GET.get('post_page')
    posts_obj = post_paginator.get_page(post_page_number)

    comment_paginator = Paginator(comments, 10)
    comment_page_number = request.GET.get('comment_page')
    comments_obj = comment_paginator.get_page(comment_page_number)

    gig_paginator = Paginator(gigs, 10)
    gig_page_number = request.GET.get('gig_page')
    gigs_obj = gig_paginator.get_page(gig_page_number)

    bug_paginator = Paginator(bugs, 10)
    bug_page_number = request.GET.get('bug_page')
    bugs_obj = bug_paginator.get_page(bug_page_number)

    context = {
    'bugs_obj' : bugs_obj,
    'comments_obj' : comments_obj,
    'posts_obj': posts_obj,
    'gigs_obj': gigs_obj,
    }

    return render (request, 'dashboard/report_list.html', context )


@superuser_required
def delete_reported_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        with transaction.atomic():
            # Generate 'fine' alert for the post's author
            print("Generating 'fine' alert for post author:", post.posted_by.username)
            Alert.objects.create(
                sender=request.user, 
                receiver=post.posted_by, 
                alert_type='fine', 
                
                is_read=False
            )
            
            # Generate 'delete' alerts for users related to the reports
            reports = Report.objects.filter(post=post)
            print("Number of reports:", reports.count())
            for report in reports:
                print("Generating 'delete' alert for user:", report.user.username)
                Alert.objects.create(
                    sender=request.user, 
                    receiver=report.user, 
                    alert_type='delete', 
                    
                    is_read=False
                )
        
        # Deduct 200 from the post owner's wallet balance and add it to their wallet's losses
        post_owner_wallet = post.posted_by.wallet
        post_owner_wallet.balance -= 200
        post_owner_wallet.losses += 200
        post_owner_wallet.save()
        
        # Delete the post object
        print("Deleting post:", post)
        post.delete()
        
        messages.success(request, 'The reported post has been deleted.')
    return redirect('reports')


@superuser_required
def delete_reported_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        
        with transaction.atomic():
            # Generate 'fine' alert for the comment's author
            Alert.objects.create(
                sender=request.user, 
                receiver=comment.comment_by, 
                alert_type='fine', 
                
                is_read=False
            )
            
            # Generate 'delete' alerts for users related to the reports
            reports = ReportComment.objects.filter(comment=comment)
            for report in reports:
                print("Generating 'delete' alert for user:", report.user.username)
                Alert.objects.create(
                    sender=request.user, 
                    receiver=report.user, 
                    alert_type='delete', 
                    
                    is_read=False
                )
        
        # Deduct 200 from the post owner's wallet balance and add it to their wallet's losses
        post_owner_wallet = comment.comment_by.wallet
        post_owner_wallet.balance -= 200
        post_owner_wallet.losses += 200
        post_owner_wallet.save()
        
        # Delete the post object
        comment.delete()
        
        messages.success(request, 'The reported post has been deleted.')
    return redirect('reports')


@superuser_required
def delete_reported_gig(request, gig_id):
    if request.method == 'POST':
        gig = get_object_or_404(Gig, id=gig_id)
        
        with transaction.atomic():
            # Generate 'fine' alert for the gig's author
            Alert.objects.create(
                sender=request.user, 
                receiver=gig.posted_by, 
                alert_type='fine', 
                
                is_read=False
            )
            
            # Generate 'delete' alerts for users related to the reports
            reports = ReportGig.objects.filter(gig=gig)
            for report in reports:
                print("Generating 'delete' alert for user:", report.user.username)
                Alert.objects.create(
                    sender=request.user, 
                    receiver=report.user, 
                    alert_type='delete', 
                    
                    is_read=False
                )
        
        # Deduct 200 from the post owner's wallet balance and add it to their wallet's losses
        post_owner_wallet = gig.posted_by.wallet
        post_owner_wallet.balance -= 200
        post_owner_wallet.losses += 200
        post_owner_wallet.save()
        
        # Delete the post object
        gig.delete()
        
        messages.success(request, 'The reported post has been deleted.')
    return redirect('reports')


@superuser_required
def delete_reported_bug(request, bug_id):
    if request.method == 'POST':
        bug = get_object_or_404(ReportBug, id=bug_id)
        
        with transaction.atomic():
            # Generate 'fine' alert for the bug's author
            Alert.objects.create(
                sender=request.user, 
                receiver=bug.user, 
                alert_type='bug', 
                
                is_read=False
            )
      
        # Delete the post object
        bug.delete()
        
        messages.success(request, 'The reported post has been deleted.')
    return redirect('reports')


@superuser_required
def keep_reported_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        # Reset the flagged field to False
        post.flagged = False
        post.save()
        
        # Generate 'keep' alerts for users with reports related to the post
        for report in post.report.all():
            Alert.objects.create(
                sender=request.user, 
                receiver=report.user, 
                alert_type='keep', 
                post=post,
                is_read=False
            )
        
        # Delete all reports related to the post
        post.report.all().delete()
        
        messages.success(request, 'The reported post has been kept.')
        
    return redirect('reports') 
    
@superuser_required
def keep_reported_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        
        # Reset the flagged field to False
        comment.flagged = False
        comment.save()
        
        # Generate 'keep' alerts for users with reports related to the comment
        for report in comment.c_report.all():
            Alert.objects.create(
                sender=request.user, 
                receiver=report.user, 
                alert_type='keep', 
                post=comment.parent_post,
                is_read=False
            )
        
        # Delete all reports related to the post
        comment.c_report.all().delete()
        
        messages.success(request, 'The reported comment has been kept.')
        
    return redirect('reports') 

@superuser_required
def keep_reported_gig(request, gig_id):
    if request.method == 'POST':
        gig = get_object_or_404(Gig, id=gig_id)
        
        # Reset the flagged field to False
        gig.flagged = False
        gig.save()
        
        # Generate 'keep' alerts for users with reports related to the gig
        for report in gig.g_report.all():
            Alert.objects.create(
                sender=request.user, 
                receiver=report.user, 
                alert_type='keep', 
                is_read=False
            )
        
        # Delete all reports related to the post
        gig.g_report.all().delete()
        
        messages.success(request, 'The reported gig has been kept.')
        
    return redirect('reports') 
    
   
 
@superuser_required
def post_article(request):
    my_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        post_form = NewArticleForm(request.POST, request.FILES)  # Include request.FILES here
        if post_form.is_valid():
            try:
                # Attempt to get the logged-in user's profile
                my_profile = Profile.objects.get(user=request.user)
            except ObjectDoesNotExist:
                pass  # Handle thea case if necessary
            
            post = post_form.save(commit=False)  # Don't commit the post yet
            post.posted_by = request.user
            post.save()
            
            return JsonResponse(res)
        else:
            res = {'success': False, 'message': 'Form data is invalid.'}
            return JsonResponse(res)
    else:
        post_form = NewArticleForm()

    context = {
    'my_profile' : my_profile,
    'post_form': post_form,

    }

    return render (request, 'dashboard/add_article.html', context )

def view_cart(request):
    context = {

    }

    return render (request, 'store/cart.html', context )
