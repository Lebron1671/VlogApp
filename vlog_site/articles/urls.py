from django.urls import path

from . import views


urlpatterns = [
   path('', views.home, name='home'),
   path('create/', views.create, name="create"),
   path('<slug:article_slug>/update/', views.update, name="update"),
   path('<slug:article_slug>/', views.detail, name='detail'),
   path('<slug:article_slug>/leave_comment/', views.leave_comment, name='leave_comment'),
   path('<slug:article_slug>/<int:comment_id>/reply_to_comment/', views.reply_to_comment, name='reply_to_comment'),
   path('category/<slug:category_slug>/', views.show_category, name='category'),
]