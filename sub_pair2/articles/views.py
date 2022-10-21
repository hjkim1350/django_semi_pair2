import django
from django.shortcuts import redirect, render
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib.auth.decorators import login_required 

# Create your views here.
def index(request):

    articles = Article.objects.order_by('-pk')

    context = {
        'articles' : articles,
    }

    return render(request, 'articles/index.html', context)


@login_required
def create(request):

    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect(request.GET.get("next") or 'articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form' : article_form
    }

    return render(request, 'articles/create.html', context)

def detail(request, pk):

    article = Article.objects.get(pk=pk)

    comment_form = CommentForm()
    
    context = {
        'article' : article,
        'comment_form' : comment_form,
        'comments' : article.comment_set.all() #해당 글의 모든 코멘트
    }

    return render(request, 'articles/detail.html', context)


def update(request, pk):

    article = Article.objects.get(pk=pk)

    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
       
    context = {
        'article_form' : article_form,
    }

    return render(request, 'articles/update.html', context)


def delete(request, pk):

    article = Article.objects.get(pk=pk)
    article.delete()

    return redirect('articles:index')


def c_create(request, pk):

    article = Article.objects.get(pk=pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('articles:detail', article.pk)


def c_delete(request, article_pk, comment_pk):

    article = Article.objects.get(pk=article_pk)

    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()

    return redirect('articles:detail', article.pk)

