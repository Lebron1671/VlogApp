from django.db.models import Count
from django.utils.text import slugify
from transliterate import translit
from articles.models import Category, Article

menu = [
    {'title': "Add article", 'url_name': 'create'},
]


class DataMixin:
    model = Article
    slug_url_kwarg = 'article_slug'
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.annotate(Count('article'))
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(0)

        context['menu'] = user_menu
        context['categories'] = categories

        if 'category_selected' not in context:
            context['category_selected'] = 0

        return context


def cyrillic_slugify(value):
    transliterated_value = translit(value, 'ru', reversed=True)
    return slugify(transliterated_value)