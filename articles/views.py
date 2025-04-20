from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Category, Article
from .forms import ArticleForm, CategoryForm, CustomUserCreationForm, CustomAuthenticationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView
from django.db.models.functions import Lower
from django.db.models import Func, F
class HomePage(ListView):
    model = Category
    template_name = 'articles/home.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            categories = Category.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            articles = Article.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            context['search_query'] = query
            context['search_categories'] = categories
            context['search_articles'] = articles
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = "articles/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        # Подкатегории
        context['subcategories'] = category.subcategories.all()
        # Статьи
        context['articles'] = category.articles.all()
        return context
class ArticleDetail(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    pk_url_kwarg = 'id'
    context_object_name = 'article'

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'articles/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'articles/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            return redirect('profile')  
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'articles/profile_form.html', {'form': form})
@login_required
def profile_view(request):
    return render(request, 'articles/profile.html')
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def article_create(request, parent_id):
    parent_category = get_object_or_404(Category, id=parent_id)
     
    if request.method == 'POST':
        form = ArticleForm(request.POST, parent_category=parent_category)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            if 'category' in form.cleaned_data:
                article.category = form.cleaned_data['category']
            else:
                article.category = parent_category
                
            article.save()
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm(parent_category=parent_category)
     
    return render(request, 'articles/article_form.html', {'form': form, 'parent': parent_category})
@login_required
@user_passes_test(is_admin)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm(instance=article)

    return render(request, 'articles/article_form.html', {
        'form': form,
        'article': article,
        'parent': article.category,
    })



@login_required
@user_passes_test(is_admin)
def category_create(request, parent_id=None):  
    parent = None
    if parent_id and parent_id != 0:
        parent = get_object_or_404(Category, id=parent_id)


    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if parent:
                category.parent = parent 
            category.save()
            return redirect(category.get_absolute_url())
    else:
        form = CategoryForm()

    return render(request, 'articles/category_form.html', {'form': form, 'parent': parent})

@login_required
@user_passes_test(is_admin)
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'articles/category_form.html', {'form': form, 'category': category})
@login_required
@user_passes_test(is_admin)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('category_detail', pk=article.category.id)  
    return render(request, 'articles/article_edit.html', {'article': article})

@require_POST
@login_required
@user_passes_test(is_admin)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    category.delete()
    if category.parent_id:
        return redirect('category_detail', pk=category.parent_id)
    return redirect('home')

def search_results_view(request):
    if request.method == "POST":
        searched = request.POST['searched']
        categories = Category.objects.filter(name__icontains = searched)
        articles = Article.objects.filter(title__icontains = searched)
    

        context = {
            'search_query': searched,
            'search_categories': categories,
            'search_articles': articles,
        }
    
    return render(request, 'articles/search_results.html', context)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Article

@csrf_exempt
def article_update_ajax(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')

        article = Article.objects.get(pk=pk)
        article.content = content
        article.save()

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'error': 'Invalid method'}, status=400)

