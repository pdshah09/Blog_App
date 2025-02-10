from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator
from .forms import CommentForm

# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('-publication_date')
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'post_list.html', {'page_obj': page_obj})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

