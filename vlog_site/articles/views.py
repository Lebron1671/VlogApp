from django.shortcuts import render
from . models import *
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

menu = ["Add article", "Log in"]

def home(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    return render(request, 'articles/index.html', {'menu': menu, 'articles': articles, 'categories': categories})


def detail(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except:
        raise Http404("The article is not found")

    article_comments_list = article.comment_set.order_by('-id')
    return render(request, 'articles/detail.html', {'article': article, 'article_comments_list': article_comments_list})


def create(request):
    if request.POST:
        category_name = request.POST.get('category')
        category = Category.objects.get(category_name=category_name)
        art_name = request.POST.get('art_name')
        art_content = request.POST.get('art_content')
        article = Article(category=category, article_title=art_name, article_content=art_content)
        article.save()
        return HttpResponseRedirect(reverse('detail', args=(article.id,)))
    else:
        categories = Category.objects.all()
        return render(request, 'articles/create.html', {'categories': categories})


def update(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.POST:
        article.article_title = request.POST['art_name']
        article.article_content = request.POST['art_content']
        category_name = request.POST.get('category')
        category = Category.objects.get(category_name=category_name)
        article.category = category
        article.save()
        return HttpResponseRedirect(reverse('detail', args=(article.id,)))
    else:
        return render(request, 'articles/update.html', {'article': article})


def delete(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except:
        raise Http404("The article is not found")

    article.delete()
    return HttpResponseRedirect(reverse('home'))


def leave_comment(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except:
        raise Http404("The article is not found")

    article.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])
    return HttpResponseRedirect(reverse('detail', args=(article_id,)))


def reply_to_comment(request, article_id, comment_id):
    try:
        article = Article.objects.get(id=article_id)
    except:
        raise Http404("The article is not found")

    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        raise Http404("The comment is not found")

    article.comment_set.create(author_name=request.POST['replier_name'], comment_text=request.POST['replier_text'], parent_comment=comment)
    return HttpResponseRedirect(reverse('detail', args=(article_id,)))
