from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from .forms import PostForm

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=0)
    template_name = "shoppinglist/index.html"
    paginate_by = 6

def post_detail(request, slug):
    """
    Display an individual :model:`shoppinglist.Post`.

    **Context**

    ``post``
        An instance of :model:`shoppinglist.Post`.

    **Template:**

    :template:`shoppinglist/post_detail.html`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    post_form = PostForm()
    return render(
        request, 
        "shoppinglist/post_detail.html",
         {"post": post,
         "post_form": post_form,},
    )