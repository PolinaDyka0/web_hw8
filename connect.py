import json
from mongoengine import connect
from models import Author, Quote

connect('mydatabase', host='mongodb+srv://userweb10:567234@cluster0.h9yiutj.mongodb.net/?retryWrites=true&w=majority')

with open('authors.json') as f:
    authors = json.load(f)

with open('quotes.json') as f:
    quotes = json.load(f)


for author in authors:
    Author(**author).save()

for quote in quotes:
    author_name = quote['author']
    author = Author.objects.get(fullname=author_name)
    quote['author'] = author
    Quote(**quote).save()