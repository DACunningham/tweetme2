from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    try:
        obj = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
    finally:
        pass

    return HttpResponse(f"<h1>Hello World: Id = {tweet_id} - {obj.content}</h1>")
