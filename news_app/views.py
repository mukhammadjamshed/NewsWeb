from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)
from .forms import ContactForm, CommentForm
from .models import Category, News
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from news_project.custom_permissions import OnlyLoggedSuperUser
from django.contrib.auth.models import User
from django.views.generic import DetailView

# your view classes here


def news_list(request):
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }

    return render(request, "news/news_list.html", context)


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    slug_url_kwarg = 'news'
    queryset = News.objects.filter(status=News.Status.Published).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.filter(active=True)
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comments = self.object.comments.filter(active=True)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = self.object
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
        else:
            new_comment = None
        context = self.get_context_data()
        context['new_comment'] = new_comment
        context['comments'] = comments
        context['comment_form'] = comment_form
        return self.render_to_response(context)


@login_required
def homePageView(request):
    categories = Category.objects.all()
    news_list = News.objects.all().order_by("-publish_time")[:5]
    local_one = News.published.filter(category__name="Mahalliy").order_by("-publish_time")[:1]
    local_news = News.published.all().filter().filter(category__name="Mahalliy")[1:6]
    context = {
        "news_list": news_list,
        "categories": categories,
        "local_one": local_one,
        "local_news": local_news

    }

    return render(request, 'news/home.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.objects.all().order_by("-publish_time")[:5]
        context['mahalliy_xabarlar'] = News.published.all().filter().filter(category__name="Mahalliy")[:5]
        context['xorij_xabarlari'] = News.published.all().filter().filter(category__name="Xorij")[:5]
        context['sport_xabarlari'] = News.published.all().filter().filter(category__name="Sport")[:5]
        context['texnologiya_xabarlari'] = News.published.all().filter().filter(category__name="Texnologiya")[:5]

        return context


def errorPageView(request):
    context = {

    }

    return render(request, 'news/404.html', context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()

            return HttpResponse("<h2> Thank for your attention</h2>")
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = News.objects.all().filter(category__name="Mahalliy")
        return news


class ForeignNewsView(ListView):
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklari'

    def get_queryset(self):
        news = News.objects.all().filter(category__name="Xorij")
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologik_yangiliklar'

    def get_queryset(self):
        news = News.objects.all().filter(category__name="Texnologiya")
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklari'

    def get_queryset(self):
        news = News.objects.all().filter(category__name="Sport")
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

@login_required
@user_passes_test(lambda u: u.is_superuser == True)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }

    return render(request, 'pages/admin_page.html', context)
