from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField('category name', max_length=50)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    article_title = models.CharField('article name', max_length=200)
    article_content = models.TextField('article content')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    mod_date = models.DateTimeField('modification date', auto_now=True)

    def __str__(self):
        return self.article_title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'article_slug': self.slug})

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['id']


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    author_name = models.CharField('author name', max_length=50)
    comment_text = models.CharField('comment text', max_length=200)
    added_date = models.DateTimeField("date added", auto_now_add=True)

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'