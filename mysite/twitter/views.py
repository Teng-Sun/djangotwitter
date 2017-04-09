from django.shortcuts import render

def tweet_list(request):
    return render(request, 'twitter/tweet_list.html', {})