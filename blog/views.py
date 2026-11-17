from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, PostForm
from .models import Category, Post


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    ordering = "-created_at"


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"


@method_decorator(staff_member_required, name="dispatch")
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_form.html"
    extra_context = {"heading": "Criar post"}

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


@method_decorator(staff_member_required, name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_form.html"
    extra_context = {"heading": "Editar post"}

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


@method_decorator(staff_member_required, name="dispatch")
class PostDeleteView(DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

@login_required(login_url="blog:login")
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = CommentForm()

    return render(
        request,
        "comment_form.html",
        {"form": form, "post": post},
    )

def category_list(request):
    categories = Category.objects.order_by("name")
    return render(request, "category_list.html", {"categories": categories})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.order_by("-created_at")

    return render(
        request,
        "post_list.html",
        {"category": category, "posts": posts},
    )