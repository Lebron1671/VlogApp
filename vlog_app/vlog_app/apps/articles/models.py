from django.db import models


class Article(models.Model):
    article_title = models.CharField('article name', max_length=200)
    article_content = models.TextField('article content')
    pub_date = models.DateTimeField('publication date')


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name = models.CharField('author name', max_length=50)
    comment_text = models.CharField('comment text', max_length=200)