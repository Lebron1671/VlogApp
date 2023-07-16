from django.shortcuts import render, get_object_or_404
from . models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.defaultfilters import slugify

def home(request):
    articles = Article.objects.all()
    return render(request, 'articles/pages/index.html', { 'articles': articles })


def detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    article_comments_list = article.comment_set.order_by('-id')

    context = {
        'article': article,
        'article_comments_list': article_comments_list,
        'category_selected': article.category_id
    }

    return render(request, 'articles/pages/detail.html', context=context)


def create(request):
    if request.POST:
        category = Category.objects.get(category_name=request.POST.get('category'))
        art_name = request.POST.get('art_name')
        art_content = request.POST.get('art_content')

        article = Article(
            category=category,
            article_title=art_name,
            article_content=art_content,
            slug=slugify(art_name)
        )
        article.save()

        return HttpResponseRedirect(reverse('detail', args=(article.slug,)))
    else:

        return render(request, 'articles/pages/create.html')


def update(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    if request.POST:
        category = Category.objects.get(category_name=request.POST.get('category'))

        article.article_title = request.POST['art_name']
        article.article_content = request.POST['art_content']
        article.category = category
        article.save()

        return HttpResponseRedirect(reverse('detail', args=(article.slug,)))
    else:

        return render(request, 'articles/pages/update.html', {'article': article })


def delete(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    article.delete()

    return HttpResponseRedirect(reverse('home'))


def leave_comment(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)

    article.comment_set.create(
        author_name=request.POST['name'],
        comment_text=request.POST['text'])

    return HttpResponseRedirect(reverse('detail', args=(article_slug,)))


def reply_to_comment(request, article_slug, comment_id):
    article = get_object_or_404(Article, slug=article_slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    article.comment_set.create(
        author_name=request.POST['replier_name'],
        comment_text=request.POST['replier_text'],
        parent_comment=comment)

    return HttpResponseRedirect(reverse('detail', args=(article_slug,)))


def show_category(request, category_slug):
    articles = Article.objects.filter(category__slug=category_slug)
    selected_category = Category.objects.get(slug=category_slug)
    context = {
        'articles' : articles,
        'category_selected': selected_category.id
    }

    return render(request, 'articles/pages/index.html', context=context)

