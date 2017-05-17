from django.contrib.auth.models import User
from twitter.models import Stream
from . import post, share


def index(request):
    user = request.user
    stream_list = []
    show_pagination = False
    if user.is_authenticated():
        streams = Stream.objects.filter(receiver=user)
        for s in streams:
            post.get_action_data(s.tweet, user)
        paginate_by = 10
        stream_list, show_pagination = share.pagination(request, streams, paginate_by)
    return {
        'stream_list': stream_list,
        'object_list': stream_list,
        'show_pagination': show_pagination,
    }