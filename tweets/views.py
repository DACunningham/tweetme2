import random
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import Tweet
from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, "components/form.html", context={"form": form}, status=200)


def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


def tweet_list_view(request, *args, **kwargs):
    """REST API VIEW

    Args:
        request (Request): Standard Request sent to a view.

    Returns:
        JsonResponse: Data for all Tweets in DB and HTTP Status of request.
    """
    qs = Tweet.objects.all()
    tweets_list = [
        {"id": x.id, "content": x.content, "likes": random.randint(0, 100000)}
        for x in qs
    ]
    data = {"isUser": False, "response": tweets_list}
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """REST API VIEW

    Args:
        request (Request): Standard Request sent to a view.
        tweet_id (int): Id of Tweet to get from DB.

    Returns:
        JsonResponse: Data for Tweet object and HTTP Status of request.
    """
    data = {
        "id": tweet_id,
    }
    status = 200

    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data["message"] = "Not Found!"
        status = 404

    return JsonResponse(data, status=status)
    # return HttpResponse(f"<h1>Hello World: Id = {tweet_id} - {obj.content}</h1>")
