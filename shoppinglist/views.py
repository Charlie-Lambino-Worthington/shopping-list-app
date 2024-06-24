from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Post
from .forms import PostForm, EditForm

class PostList(LoginRequiredMixin, generic.ListView):
    template_name = "shoppinglist/index.html"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.add_message(request, messages.SUCCESS, 'New post created!')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Error creating post.')
            return self.get(request, *args, **kwargs)

@login_required
def post_detail(request, slug):
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, slug=slug)
    post_form = PostForm()
    edit_form = EditForm(instance=post)
    return render(request, "shoppinglist/post_detail.html", {"post": post, "post_form": post_form, "edit_form": edit_form})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Post deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You do not have permission to delete this post.')
    return HttpResponseRedirect(reverse('home'))

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        edit_form = EditForm(request.POST, instance=post)
        if edit_form.is_valid() and post.author == request.user:
            edit_form.save()
            messages.add_message(request, messages.SUCCESS, 'Post updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating post!')
    return HttpResponseRedirect(reverse('post_detail', args=[slug]))
