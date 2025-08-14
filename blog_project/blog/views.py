# blog/views.py
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
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
    fields = ['title', 'content', 'category', 'image']
    template_name = 'blog/post_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # add message when form is valid
        messages.success(self.request, 'Your post has been created successfully!')
        return response
    
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # New class created and UpdateView passed in.
  model = Post
  fields = ['title', 'content', 'category', 'image']
  template_name = 'blog/post_update.html'
    
  def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Your post has been updated!')
        return response
  
  #Added a new function here to check the user author is correct for the spefice Post.
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False
  
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