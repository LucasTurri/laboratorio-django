from django.contrib.auth.views import LoginView
from django.urls import path

from . import views


app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("posts/novo/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/editar/", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/remover/", views.PostDeleteView.as_view(), name="post_delete"),
    path("entrar/", LoginView.as_view(template_name="login.html"), name="login"),
    path("posts/<int:pk>/comentar/", views.comment_create, name="comment_create"),
    path("categorias/", views.category_list, name="category_list"),
    path("categorias/<int:pk>/", views.category_detail, name="category_detail"),
]