from multiprocessing import context
from symtable import Class

from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from news_app.models import News, Category
from .forms import ContactForm

# Create your views here.


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(
            status=News.Status.Published
        )



class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    slug_url_kwarg = 'news'
    def get_queryset(self):
        return News.objects.filter(
            status=News.Status.Published
        )


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_data'] = Category.objects.all()
        context['news_list'] = News.objects.all().order_by('-published_time')[:10]
        context['sport_data'] = News.objects.filter(category__name = 'Sport')[:5]
        context['tech_data'] = News.objects.filter(category__name = 'Texnologiya')[:5]
        return context

def contactPageView(request):
    form = ContactForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse('<h2> Biz bilan boglaningiz uchun rahamt </h2>')
    context = {'form':form}
    return render(request, 'news/contact.html',context)

class JahonPageView(ListView):
    model=News
    template_name ='news/jahon_news.html'
    context_object_name = 'jahon_list'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name = 'Jahon')
        return news

class IqsodiyotPageView(ListView):
    model=News
    template_name ='news/iqsodiyot_news.html'
    context_object_name = 'iqsodiyot_list'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name = 'Iqsodiyot')
        return news