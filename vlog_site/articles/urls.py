from django.urls import path

from . import views


urlpatterns = [
   path('', views.home, name='home'),
   path('create/', views.create, name="create"),
   path('<int:article_id>/update/', views.update, name="update"),
   path('<int:article_id>/', views.detail, name='detail'),
   path('<int:article_id>/leave_comment/', views.leave_comment, name='leave_comment'),
   path('<int:article_id>/<int:comment_id>/reply_to_comment/', views.reply_to_comment, name='reply_to_comment'),
]