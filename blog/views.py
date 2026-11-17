from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post


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