from multiprocessing import context

from .models import News, Category


def categories(request):
    categories1 = Category.objects.all()[:2]
    context = {
        'categories1':categories1
    }
    return context