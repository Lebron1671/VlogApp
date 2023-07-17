from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from .forms import *
from .models import *
from articles.utils import *
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticlesHome(DataMixin, ListView):
    template_name = 'articles/pages/index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Article.objects.order_by('-id').select_related('category')


class CreateArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddArticleForm
    template_name = 'articles/pages/create.html'
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self,*,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        slug = cyrillic_slugify(form.cleaned_data['article_title'])
        form.instance.slug = slug

        return super().form_valid(form)


class ShowArticle(DataMixin, DetailView):
    template_name = 'articles/pages/detail.html'
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(category_selected=context['article'].category_id)

        return dict(list(context.items()) + list(c_def.items()))


class UpdateArticle(DataMixin, UpdateView):
    template_name = 'articles/pages/update.html'
    fields = ['article_title', 'article_content', 'category', 'photo']
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(category_selected=context['article'].category_id)

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        slug = cyrillic_slugify(form.cleaned_data['article_title'])
        form.instance.slug = slug

        return super().form_valid(form)


class DeleteArticle(DataMixin, DeleteView):
    template_name = 'articles/pages/delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(category_selected=context['article'].category_id)

        return dict(list(context.items()) + list(c_def.items()))


class ArticlesCategory(DataMixin, ListView):
    template_name = 'articles/pages/index.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(category_selected=context['articles'][0].category_id)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Article.objects.filter(category__slug=self.kwargs['category_slug']).select_related('category')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'articles/pages/register.html'
    success_url = reverse_lazy('login')

    def get_user_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'articles/pages/login.html'

    def get_user_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class FeedbackFormView(DataMixin, FormView):
    form_class = FeedbackForm
    template_name = 'articles/pages/feedback.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        return dict(list(context.items()) + list(c_def.items()))


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


"""
def show_category(request, category_slug):
    articles = Article.objects.filter(category__slug=category_slug)
    selected_category = Category.objects.get(slug=category_slug)
    context = {
        'articles' : articles,
        'category_selected': selected_category.id
    }

    return render(request, 'articles/pages/index.html', context=context)

def home(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 3)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'articles/pages/index.html', {'page_obj': page_obj })


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


def detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    article_comments_list = article.comment_set.order_by('-id')

    context = {
        'article': article,
        'article_comments_list': article_comments_list,
        'category_selected': article.category_id
    }

    return render(request, 'articles/pages/detail.html', context=context)

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
"""