from django.db import models


class Category(models.Model):
    text = models.CharField(max_length=50)


class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.BigIntegerField(db_index=True)
    img = models.CharField(max_length=200, default="")
    link = models.CharField(max_length=200, db_index=True)
    hidden = models.CharField(max_length=100)


class Question(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_ans = models.BooleanField()
