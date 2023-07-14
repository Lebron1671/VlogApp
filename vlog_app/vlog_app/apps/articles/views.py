from django.shortcuts import render
from . models import Article, Comment
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from . forms import CreateNewArticle


def home(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'articles/list.html', {'latest_articles_list': latest_articles_list})


def create(request):
    if request.POST:
        created_date = timezone.now()
        new_article = Article(article_title=request.POST['art_name'], article_content=request.POST['art_content'], pub_date=created_date, mod_date=created_date)
        new_article.save()
        return HttpResponseRedirect(reverse('articles:detail', args=(new_article.id,)))
    else:
        return render(request, 'articles/create.html')


def update(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.POST:
        article.article_title = request.POST['art_name']
        article.article_content = request.POST['art_content']
        article.mod_date=timezone.now()
        article.save()
        return HttpResponseRedirect(reverse('articles:detail', args=(article.id,)))
    else:
        return render(request, 'articles/update.html', {'article': article})


def delete(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except:
        raise Http404("The article is not found")

    article.delete()
    return HttpResponseRedirect(reverse('articles:home'))


def detail(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except:
        raise Http404("The article is not found")

    latest_comments_list = article.comment_set.order_by('-id')[:10]
    return render(request, 'articles/detail.html', {'article': article, 'latest_comments_list': latest_comments_list})


def leave_comment(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except:
        raise Http404("The article is not found")

    article.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'], added_date=timezone.now())
    return HttpResponseRedirect(reverse('articles:detail', args=(article_id,)))

def reply_to_comment(request, article_id, comment_id):
    try:
        article = Article.objects.get(id=article_id)
    except:
        raise Http404("The article is not found")

    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        raise Http404("The comment is not found")

    article.comment_set.create(author_name=request.POST['replier_name'], comment_text=request.POST['replier_text'],added_date=timezone.now(), parent_comment=comment)
    return HttpResponseRedirect(reverse('articles:detail', args=(article_id,)))