import stripe

from django.shortcuts import render
from django.utils import timezone

from pages.models import Pages
from blog.models import Post

def redirect_root(request):
    posts           = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:1]
    last_post_id    = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:1][0].id
    pages           = Pages.objects.order_by('order')
    return render(request, 'blog/post_list.html', { 'posts': posts, 'pages': pages, 'id' : last_post_id })

def redirect_research(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/blog_research.html', { 'pages': pages })


def redirect_coffee(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/blog_coffee.html', { 'pages': pages })


def redirect_coffee_confirm(request):
    stripe.api_key = "sk_live_0fHEU5T1nHoILQpYZ7lyPwP7"

    if request.method == "POST":
        token    = request.POST.get("stripeToken")
        donation = request.POST.get("donation")

    try:
        charge  = stripe.Charge.create(
            amount      = donation,
            currency    = "usd",
            source      = token,
            description = "A generous donation from a fan!"
        )

        # new_car.charge_id   = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        #new_car.save()
        donation = int(donation) / 100.00
        return render(request, 'blog/thanks.html', { 'donation' : donation })
        # The payment was successfully processed & the user's card was charged - confirm with them how much