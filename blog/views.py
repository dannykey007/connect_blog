
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.db.models import Q


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    success_url = '/'



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'video', 'video_url']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'video', 'video_url']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def contact(request):
    return render(request, 'blog/contact.html', {'title': 'Contact'})

# Line of code: The AJAX like function


def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'total_likes': post.likes.count(), 'liked': liked})


def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        # Line of code: Explicitly setting is_hidden=False to fix the IntegrityError
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            is_hidden=False
        )
        return JsonResponse({
            'author': comment.author.username,
            'content': comment.content,
            'comment_count': post.comments.count(),
            'date_posted': comment.date_posted.strftime('%b %d, %Y, %I:%M %p')
        })
    return redirect('blog-home')


def get_liked_users(request, pk):
    """Get list of users who liked a post"""
    post = get_object_or_404(Post, id=pk)
    likes = post.likes.all()

    liked_users = []
    for user in likes:
        liked_users.append({
            'username': user.username,
            'profile_image': user.profile.image.url if hasattr(user, 'profile') else '/media/default.jpg'
        })

    current_user_liked = post.likes.filter(
        id=request.user.id).exists() if request.user.is_authenticated else False

    return JsonResponse({
        'total_likes': post.likes.count(),
        'liked': current_user_liked,
        'users': liked_users
    })


def like_comment(request, pk):
    """Like a specific comment"""
    comment = get_object_or_404(Comment, id=pk)

    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    return JsonResponse({
        'total_likes': comment.likes.count(),
        'liked': liked
    })


def delete_comment(request, pk):
    """Delete a comment - only comment author can delete"""
    comment = get_object_or_404(Comment, id=pk)

    # Check if user is the comment author
    if request.user != comment.author:
        return JsonResponse({'error': 'You can only delete your own comments'}, status=403)

    post_id = comment.post.id
    comment.delete()

    return redirect('post-detail', pk=post_id)


def hide_comment(request, pk):
    """Hide/Show a comment - only post author can hide comments"""
    comment = get_object_or_404(Comment, id=pk)
    post = comment.post

    # Check if user is the post author
    if request.user != post.author:
        return JsonResponse({'error': 'Only the post author can hide comments'}, status=403)

    comment.is_hidden = not comment.is_hidden
    comment.save()

    return redirect('post-detail', pk=post.id)
