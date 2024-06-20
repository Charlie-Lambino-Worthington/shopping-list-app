from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Post
from .forms import PostForm
# Create your views here.
class PostList(LoginRequiredMixin, generic.ListView):
    template_name = "shoppinglist/index.html"
    paginate_by = 6
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
@login_required
def post_detail(request, slug):
    """
    Display an individual :model:`shoppinglist.Post`.
    **Context**
    ``post``
        An instance of :model:`shoppinglist.Post`.
    **Template:**
    :template:`shoppinglist/post_detail.html`
    """
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, slug=slug)
    post_form = PostForm()
    return render(
        request,
        "shoppinglist/post_detail.html",
         {"post": post,
         "post_form": post_form,},
    )
@login_required
def create_list(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PostForm()
    context = {"form" : form}
    return render(request, "home", context)
@login_required
def post_delete(request, slug):
    """
    Delete an individual post.
    **Context**
    ``post``
        An instance of :model:`blog.Post`.
    """
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Post deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You do not have permission to delete this post.')
    return HttpResponseRedirect(reverse('home'))