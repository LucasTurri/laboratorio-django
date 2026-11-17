from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.order_by("-created_at")
    return render(request, "post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "post_detail.html", {"post": post})

@staff_member_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = PostForm()

    return render(
        request,
        "post_form.html",
        {"heading": "Criar post", "form": form},
    )


@staff_member_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "post_form.html",
        {"heading": "Editar post", "form": form, "post": post},
    )

@staff_member_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect("blog:post_list")

    return render(request, "post_confirm_delete.html", {"post": post})