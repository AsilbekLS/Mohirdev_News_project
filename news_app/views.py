from multiprocessing import context
from symtable import Class

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Model, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin

from accounts.custom_permissions import IsAdminUser
from news_app.models import News, Category
from .forms import ContactForm, CommentForm

# Create your views here.


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(
            status=News.Status.Published
        )




def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    #hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    context['hitcount'] = {'pk': hit_count.pk}
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits



    comments = news.comment.filter(active=True)
    comment_count = comments.count()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #yangi komment obyektini yaratamiz lekin DB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            #izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # ma'lumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        'comments': comments,
        'comment_count': comment_count,
        'comment_form': comment_form
    }

    return render(request, 'news/news_detail.html', context)





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

class NewsUpdateView(IsAdminUser,UpdateView):
    model = News
    template_name = 'crud/news_update.html'
    fields = ['title','body','image','category','status']

class NewsDeleteView(IsAdminUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page_view')

class NewsCreateNews(IsAdminUser,CreateView):
    model = News
    template_name = 'crud/news_create.html'
   
    fields = ['title','slug','body','image','category','status']



@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    admins = User.objects.filter(is_superuser=True)
    return render(request,'pages/admin_page.html',{'admins':admins} )


class SearchResultList(ListView):
    model = News
    template_name='news/search_results.html'
    context_object_name = 'all_data'

    def get_queryset(self):
        query=self.request.GET.get('q')
        return News.objects.filter(

            Q(title__icontains=query) | Q(body__icontains=query)

        )