# blog/views.py
import cloudinary.uploader
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse #for live search bar
from django.shortcuts import render
from blog.models import Post, Comment
from blog.forms import CommentForm, PostUpdateForm, PostCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, #Added here, note if you have a long line of imports you can add ( ) to move each to a new line
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


# Home Page
class PostListView(ListView):
  model = Post
  template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
  context_object_name = 'posts' #Updated here. Now the default name is set equal to 'posts'
  ordering = ['-date_posted'] 

# Details Page
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all().order_by('-created_on')
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """Handle adding a comment"""
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user.profile
            comment.save()
            messages.success(request, "💬 Your comment has been added!")
            return redirect('blog:post_detail', pk=self.object.pk)

        # If form invalid, re-render page with errors
        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)

# Create page
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_new.html'

    def form_valid(self, form):
        # Set the author
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # Success message
        messages.success(self.request, 'Your post has been created successfully!')
        return response

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'blog/post_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        # Preserve existing image if no new image uploaded
        if not form.cleaned_data.get('image') and self.object.image:
            form.instance.image = self.object.image

        response = super().form_valid(form)
        messages.success(self.request, 'Your post has been updated!')
        return response

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("blog:blog_index")  # ✅ Redirect to blog homepage

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        messages.success(self.request,
            f"✅ Your post '{post.title}' has been deleted."
        )
        return super().delete(request, *args, **kwargs)
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_delete.html"

    def get_success_url(self):
        # Redirect back to the post detail page after deletion
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Only allow deletion if the logged-in user is the comment's author
        comment = self.get_object()
        return self.request.user == comment.author.user

# user can only see his posts when logged in    
class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_posts.html"  
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_posted')


def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:5]  # limit results
        suggestions = [{'title': post.title, 'url': post.get_absolute_url()} for post in posts]
    return JsonResponse(suggestions, safe=False)