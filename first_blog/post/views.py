from django.db.models import Q
from urllib.parse import quote_plus
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect,Http404
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.utils import timezone


def post_update(request, pk):
    instance = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, '<a href="#">Item</a> updated', extra_tags='html_safe')
        print(messages)
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {
        'form':form
    }
    return render(request, 'post_form.html', context)

def create_post(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form':form
    }
    return render(request, 'post_form.html', context)


def post_list(request):
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset_list = queryset.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
        ).distinct()
    # paginator = Paginator(queryset_list,1) # Show 25 contacts per page
    # page = request.GET.get('page')
    # posts = paginator.get_page(page)

    paginator = Paginator(queryset_list, 4) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
	    queryset = paginator.page(page)

    except PageNotAnInteger:
        queryset = paginator.page(1)

    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
		

    context = {
        'object_list':queryset,
        'posts': page,
        "page_request_var": page_request_var,
    }
    return render(request, 'index.html', context)


def detail(request,pk):
    obj = get_object_or_404(Post, id=pk)
    share_string = quote_plus(obj.content)
    context = {
        'title':obj.title,
        'instance':obj,
        'share_string':share_string
    }
    return render(request, 'detail.html', context)


def delete(request,pk):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=pk)
    instance.delete()
    messages.success(request, "Successfuly Deleted")
    return redirect('post:post_list')
