from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Category, Post, Subscription
from django.shortcuts import get_object_or_404
from datetime import datetime
from .filters import PostFilter
from .forms import CreateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = '-date_published'
    paginate_by = 5


class SearchPost(ListView):
    model = Post
    ordering = '-date_published'
    template_name = 'postsearch.html'
    context_object_name = 'postsearch'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class CategoryView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category)
        return queryset


class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = CreateForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('news_list')

    def post_create(request):
        if request.method == 'POST':
            form = CreateForm(request.POST)
            if form.is_valid():
                form.instance.category_id = request.POST.get('category_id')
                form.save()
                return redirect('home')
        else:
            form = CreateForm()

        context = {'form': form}
        return render(request, 'post_create.html', context)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.post_delete',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )






