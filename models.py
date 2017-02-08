from mongoengine import *

DB_NAME = 'hseproject'
CATS = ["Россия", "Мир", "Бывший СССР", "Финансы", "Бизнес", "Силовые структуры",
        "Наука и техника", "Культура", "Спорт", "Интернет и СМИ", "Ценности",
        "Путешествия", "Из жизни"]


class Category(Document):
    text = StringField(unique=True)


class News(Document):
    category = ReferenceField(Category)
    title = StringField()
    text = StringField()
    date = StringField()
    img = StringField()
    link = StringField()


def init_category():
    if Category.objects.count() == 0:
        for cat in CATS:
            Category(text=cat).save()


def clear_database():
    for t in News.objects:
        t.delete()

    for t in Category.objects:
        t.delete()

