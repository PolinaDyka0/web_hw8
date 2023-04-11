import redis
from models import Author, Quote
from mongoengine import connect
import time

connect('mydatabase', host='mongodb+srv://userweb10:567234@cluster0.h9yiutj.mongodb.net/?retryWrites=true&w=majority')

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def search_by_author_cached(author_name):
    # Зберігаємо результати в Redis, якщо вони ще не збережені
    if not redis_client.exists(author_name):
        authors = Author.objects(fullname__istartswith=author_name)
        quotes = []
        for author in authors:
            author_quotes = Quote.objects(author=author)
            quotes.extend(author_quotes)
        if quotes:
            quotes_str = '\n'.join([quote.quote for quote in quotes])
            redis_client.set(author_name, quotes_str)
        else:
            redis_client.set(author_name, "")
    # Повертаємо результати з Redis
    return redis_client.get(author_name).decode('utf-8')


def search_by_tag_cached(tag):
    # Зберігаємо результати в Redis, якщо вони ще не збережені
    if not redis_client.exists(tag):
        quotes = Quote.objects(tags__startswith=tag)
        if quotes:
            quotes_str = '\n'.join([quote.quote for quote in quotes])
            redis_client.set(tag, quotes_str)
        else:
            redis_client.set(tag, "")
    # Повертаємо результати з Redis
    return redis_client.get(tag).decode('utf-8')

def search_by_tags_cached(tags):
    # Зберігаємо результати в Redis, якщо вони ще не збережені
    if not redis_client.exists(tags):
        tags_list = tags.split(',')
        print(tags_list)
        quotes = Quote.objects(tags__all=tags_list)
        if quotes:
            quotes_str = '\n'.join([quote.quote for quote in quotes])
            redis_client.set(tags, quotes_str)
        else:
            redis_client.set(tags, "")
    # Повертаємо результати з Redis
    return redis_client.get(tags).decode('utf-8')



while True:
    user_input = input('Enter command: ')
    start_time = time.time()
    command_parts = user_input.split(':')
    command = command_parts[0].strip()
    if command == 'name':
        author_name = command_parts[1].strip()
        result = search_by_author_cached(author_name)
        print(result)
    elif command == 'tag':
        tag = command_parts[1].strip()
        result = search_by_tag_cached(tag)
        print(result)
    elif command == 'tags':
        tags = command_parts[1].strip()
        result = search_by_tags_cached(tags)
        print(result)
    elif command == 'exit':
        break
    elif command == 'clear':
        redis_client.flushdb()
    else:
        print('Invalid command')
    print(f"Execution time: {time.time() - start_time} seconds")
