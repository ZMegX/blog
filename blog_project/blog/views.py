# blog/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from blog.models import Post, Comment
from blog.forms import CommentForm
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

# Create page

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'blog/post_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Your post has been created successfully!')
        return response
    
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # New class created and UpdateView passed in.
  model = Post
  fields = ['title', 'content', 'category']
  template_name = 'blog/post_update.html'
    
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
  
  #Added a new function here to check the user author is correct for the spefice Post.
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False
  
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # New class PostDeleteView created here
  model = Post
  success_url = "/blog" # Here we are redirecting the user back to the homepage after deleting a Post successfully
  template_name = 'blog/post_delete.html'
  success_url = reverse_lazy('blog_index')

  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False