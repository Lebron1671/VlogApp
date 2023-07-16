from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import *
from . models import *
from django.utils.text import slugify
from transliterate import translit


class ArticlesHome(ListView):
    model = Article
    template_name = 'articles/pages/index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_selected'] = 0
        return context


"""
def home(request):
    articles = Article.objects.all()
    return render(request, 'articles/pages/index.html', { 'articles': articles })
"""


class ShowArticle(DetailView):
    model = Article
    template_name = 'articles/pages/detail.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_selected'] = context['article'].category_id
        return context


"""
def detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    article_comments_list = article.comment_set.order_by('-id')

    context = {
        'article': article,
        'article_comments_list': article_comments_list,
        'category_selected': article.category_id
    }

    return render(request, 'articles/pages/detail.html', context=context)
"""


class CreateArticle(CreateView):
    form_class = AddArticleForm
    template_name = 'articles/pages/create.html'

    def form_valid(self, form):
        slug = cyrillic_slugify(form.cleaned_data['article_title'])
        form.instance.slug = slug

        return super().form_valid(form)


"""
def create(request):
    if request.POST:
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                slug = cyrillic_slugify(form.cleaned_data['article_title'])
                Article.objects.create(
                    **form.cleaned_data,
                    slug=slug
                )

                return HttpResponseRedirect(reverse('detail', args=(slug,)))
            except:
                form.add_error(None, 'Error while adding new article')
    else:
        form = AddArticleForm()
        return render(request, 'articles/pages/create.html', {'form': form})
"""


class UpdateArticle(UpdateView):
    model = Article
    template_name = 'articles/pages/update.html'
    fields = ['article_title', 'article_content', 'category', 'photo']
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def form_valid(self, form):
        slug = cyrillic_slugify(form.cleaned_data['article_title'])
        form.instance.slug = slug

        return super().form_valid(form)

"""
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
"""



class DeleteArticle(DeleteView):
    model = Article
    template_name = 'articles/pages/delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'article'
    slug_url_kwarg = 'article_slug'

"""
def delete(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    article.delete()

    return HttpResponseRedirect(reverse('home'))
"""



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


class ArticlesCategory(ListView):
    model = Article
    template_name = 'articles/pages/index.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_selected'] = context['articles'][0].category_id
        return context

    def get_queryset(self):
        return Article.objects.filter(category__slug=self.kwargs['category_slug'])


"""
def show_category(request, category_slug):
    articles = Article.objects.filter(category__slug=category_slug)
    selected_category = Category.objects.get(slug=category_slug)
    context = {
        'articles' : articles,
        'category_selected': selected_category.id
    }

    return render(request, 'articles/pages/index.html', context=context)
"""


def cyrillic_slugify(value):
    # Transliterate Cyrillic characters to Latin
    transliterated_value = translit(value, 'ru', reversed=True)

    # Remove any special characters and convert to lowercase
    slug = slugify(transliterated_value)

    return slug