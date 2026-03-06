from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
