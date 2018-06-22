from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from .models import Pages
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

# Create your views here.
def pages_base(request, slug):
	pages = Pages.objects.order_by('order')
	page = Pages.objects.filter(slug=slug)
	page = get_object_or_404(Pages, pk=page[0].id)
	page.page_views += 1;
	page.save()
	return render(request, 'pages_base.html', {'page': page, 'pages': pages})