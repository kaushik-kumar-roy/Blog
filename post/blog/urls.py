"""
Blog Urls
"""
from django.urls import path

from .views import (
    blog_post_detail_page,
    blog_post_list_view,
    blog_post_create_view,
    blog_post_update_view,
    blog_post_delete_view,
    comment_create
)

urlpatterns = [
    path('create/',blog_post_create_view),
    path('<str:slug>/update/',blog_post_update_view),
    path('<str:slug>/delete/',blog_post_delete_view),
    path('', blog_post_list_view),
    path('<str:slug>/',blog_post_detail_page),
    path('<str:slug>/comment/',comment_create),
]
