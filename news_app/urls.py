from django.urls import path
from django.views import View

from .views import NewsListView, HomePageView, contactPageView, JahonPageView, IqsodiyotPageView, \
    NewsUpdateView, NewsDeleteView, NewsCreateNews, admin_page, news_detail, SearchResultList

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page_view'),
    path('contact/', contactPageView, name='contact_page_view'),
    path('news/', NewsListView.as_view(), name='all_news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),
    path('jahon-news/',JahonPageView.as_view(), name='jahon_news_page'),
    path('iqsodiyot-news/', IqsodiyotPageView.as_view(), name='iqsodiyot_news_page'),
    path('news/<slug>/update' ,NewsUpdateView.as_view(), name = 'news_update'),
    path('news/<slug>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('news/create', NewsCreateNews.as_view(), name='news_create'),
    path('searchresult/', SearchResultList.as_view(), name='search_results'),
    path('adminpage/', admin_page, name='admin_page')
]
