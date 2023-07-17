from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
   path('', views.ArticlesHome.as_view(), name='home'),
   path('register/', views.RegisterUser.as_view(), name='register'),
   path('login/', views.LoginUser.as_view(), name='login'),
   path('logout/', views.logout_user, name='logout'),
   path('feedback/', views.FeedbackFormView.as_view(), name="feedback"),
   path('create/', views.CreateArticle.as_view(), name="create"),
   path('<slug:article_slug>/update/', views.UpdateArticle.as_view(), name="update"),
   path('<slug:article_slug>/', views.ShowArticle.as_view(), name='detail'),
   path('<slug:article_slug>/delete/', views.DeleteArticle.as_view(), name="delete"),
   path('<slug:article_slug>/leave_comment/', views.leave_comment, name='leave_comment'),
   path('<slug:article_slug>/<int:comment_id>/reply_to_comment/', views.reply_to_comment, name='reply_to_comment'),
   path('category/<slug:category_slug>/', views.ArticlesCategory.as_view(), name='category'),
]