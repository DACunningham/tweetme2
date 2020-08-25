import random
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid():
        obj = serializer.save(user=request.user)
        # print(obj)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse({}, status=400)


# Create your views here.
def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()

        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)

        form = TweetForm()

    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, "components/form.html", context={"form": form}, status=200)


def home_view(request, *args, **kwargs):
    print(request.user or None)
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
    tweets_list = [x.serialize() for x in qs]
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
