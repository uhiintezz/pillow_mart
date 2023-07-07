from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import CommentForm

def comment_read(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)


class PostListView(ListView):
    model = Post
    paginate_by = 4
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'blog'
        return context

class Search(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Search <{}>".format(self.request.GET.get('s'))
        # context['s'] = f's={self.request.GET.get("s")}&'
        return context





class PostByCategory(ListView):
    paginate_by = 2
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['cat_slug'])
        return context



class PostByTag(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(Tag.objects.get(slug=self.kwargs['tag_slug']))
        return context



class PostDetailView(DetailView):
    model = Post
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['title'] = str(self.object)
        return context



class CreateComment(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()




