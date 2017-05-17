from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def pagination(request, object_list, paginate_by):
    paginator = Paginator(object_list, paginate_by)
    page = request.GET.get('page', 1)
    try:
        text = paginator.page(page)
    except PageNotAnInteger:
        text = paginator.page(1)
    except EmptyPage:
        text = paginator.page(paginator.num_pages)
    if paginator.num_pages == 1:
        show_pagination = False
    else:
        show_pagination = True
    return text, show_pagination