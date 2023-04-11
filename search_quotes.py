from models import Author, Quote
from mongoengine import connect
import sys

connect('mydatabase', host='mongodb+srv://userweb10:567234@cluster0.h9yiutj.mongodb.net/?retryWrites=true&w=majority')

def search_by_author(author_name):
    author = Author.objects.get(fullname=author_name)
    quotes = Quote.objects(author=author)
    for quote in quotes:
        print(quote.quote.encode('utf-8').decode('utf-8'))

def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    for quote in quotes:
        print(quote.quote.encode('utf-8').decode('utf-8'))

def search_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    for quote in quotes:
        print(quote.quote.encode('utf-8').decode('utf-8'))
        
while True:
    user_input = input().split(':')
    command = user_input[0].strip()
    if command == 'name':
        author_name = user_input[1].strip()
        search_by_author(author_name)
    elif command == 'tag':
        tag = user_input[1].strip()
        search_by_tag(tag)
    elif command == 'tags':
        tags = user_input[1].strip()
        search_by_tags(tags)
    elif command == 'exit':
        sys.exit()
