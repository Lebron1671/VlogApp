from django.urls import path

from . import views


app_name = 'articles'
urlpatterns = [
   path('', views.home, name='home'),
   path('create/', views.create, name="create"),
   path('<int:article_id>/update/', views.update, name="update"),
   path('<int:article_id>/delete/', views.delete, name="delete"),
   path('<int:article_id>/', views.detail, name='detail'),
   path('<int:article_id>/leave_comment/', views.leave_comment, name='leave_comment'),
]