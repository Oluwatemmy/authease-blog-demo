from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.conf import settings
from .models import Post, Comment, Like


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(user=request.user).exists()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'is_liked': is_liked,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            Post.objects.create(author=request.user, title=title, content=content)
            messages.success(request, 'Post created!')
            return redirect('home')
        messages.error(request, 'Title and content are required.')
    return render(request, 'blog/post_form.html', {'action': 'Create'})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, 'Post updated!')
            return redirect('post-detail-view', pk=post.pk)
        messages.error(request, 'Title and content are required.')
    return render(request, 'blog/post_form.html', {'action': 'Edit', 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
        return redirect('home')
    return render(request, 'blog/confirm_delete.html', {'post': post})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('post-detail-view', pk=pk)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('post-detail-view', pk=pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
    return redirect('post-detail-view', pk=post_pk)


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})


# --- OAuth Views ---

def github_login(request):
    """Redirect to GitHub's OAuth authorization page."""
    client_id = getattr(settings, 'GITHUB_CLIENT_ID', '')
    if not client_id:
        messages.error(request, 'GitHub OAuth is not configured.')
        return redirect('authease-login')
    callback_url = request.build_absolute_uri('/oauth/github/callback/')
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={callback_url}"
        f"&scope=user:email"
    )
    return redirect(github_auth_url)


def github_callback(request):
    """Handle GitHub OAuth callback, log the user in."""
    code = request.GET.get('code')
    if not code:
        messages.error(request, 'GitHub authentication failed.')
        return redirect('authease-login')

    try:
        from authease.oauth.github import Github
        from authease.oauth.utils import register_social_user

        access_token = Github.exchange_code_for_token(code)
        if not access_token:
            messages.error(request, 'Failed to get access token from GitHub.')
            return redirect('authease-login')

        user_data = Github.retrieve_github_user(access_token)
        email = user_data.get('email')
        if not email:
            messages.error(request, 'A public email is required on your GitHub account.')
            return redirect('authease-login')

        full_name = user_data.get('name') or ''
        names = full_name.split(' ', 1)
        first_name = names[0] if names[0] else email.split('@')[0]
        last_name = names[1] if len(names) > 1 else ''

        register_social_user('github', email, first_name, last_name)

        User = get_user_model()
        user = User.objects.get(email=email)
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}!')
        return redirect('home')

    except Exception as e:
        messages.error(request, f'GitHub login failed: {e}')
        return redirect('authease-login')


def google_login(request):
    """Redirect to Google's OAuth authorization page."""
    client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    if not client_id:
        messages.error(request, 'Google OAuth is not configured.')
        return redirect('authease-login')
    callback_url = request.build_absolute_uri('/oauth/google/callback/')
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={callback_url}"
        f"&response_type=code"
        f"&scope=openid+email+profile"
        f"&access_type=offline"
    )
    return redirect(google_auth_url)


def google_callback(request):
    """Handle Google OAuth callback, exchange code for tokens, log the user in."""
    code = request.GET.get('code')
    if not code:
        messages.error(request, 'Google authentication failed.')
        return redirect('authease-login')

    try:
        import requests as http_requests
        from authease.oauth.utils import register_social_user

        # Exchange code for tokens
        callback_url = request.build_absolute_uri('/oauth/google/callback/')
        token_response = http_requests.post('https://oauth2.googleapis.com/token', data={
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': getattr(settings, 'GOOGLE_CLIENT_SECRET', ''),
            'redirect_uri': callback_url,
            'grant_type': 'authorization_code',
        })
        token_data = token_response.json()
        id_token_str = token_data.get('id_token')
        if not id_token_str:
            messages.error(request, 'Failed to get token from Google.')
            return redirect('authease-login')

        # Validate the ID token using authease's Google class
        from authease.oauth.utils import Google
        google_user_data = Google.validate(id_token_str)

        if not google_user_data or google_user_data.get('aud') != settings.GOOGLE_CLIENT_ID:
            messages.error(request, 'Google authentication failed.')
            return redirect('authease-login')

        email = google_user_data['email']
        first_name = google_user_data.get('given_name', '')
        last_name = google_user_data.get('family_name', '')

        register_social_user('google', email, first_name, last_name)

        User = get_user_model()
        user = User.objects.get(email=email)
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}!')
        return redirect('home')

    except Exception as e:
        messages.error(request, f'Google login failed: {e}')
        return redirect('authease-login')
