import stripe

from django.shortcuts import render
from django.utils import timezone

from pages.models import Pages
from blog.models import Post
from quiz.models import Question
from fluency.models import Flashcard

from django.http import JsonResponse
from django.core import serializers

from django.core.mail import send_mail

def redirect_root(request):
    posts           = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:1]
    last_post_id    = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:1][0].id
    pages           = Pages.objects.order_by('order')
    return render(request, 'blog/post_list.html', { 'posts': posts, 'pages': pages, 'id' : last_post_id })

def redirect_study(request):
    pages           = Pages.objects.order_by('order')
    return render(request, 'quiz/study.html', { 'pages': pages })

def redirect_research(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/blog_research.html', { 'pages': pages })

def redirect_error_report(request):

    #send_mail('Subject here','Here is the message.','alex@behaviorist.tech',['alex@behaviorist.tech'],fail_silently=False,)
    description = request.POST.get("description")
    categories  = request.POST.getlist("categories")
    module      = request.POST.get("module")
    item_id     = request.POST.get("id")
    item        = item_id

    question_id = str(item_id)

    if module == "quiz":
        question = Question.objects.filter(pk=item_id)
        item = str(question[0])

        question = Question.objects.get(pk=item_id)
        question.error_reports += 1
        question.save()
    else:
        flashcard = Flashcard.objects.filter(pk=item_id)
        item = str(flashcard[0])

        flashcard = Flashcard.objects.get(pk=item_id)
        flashcard.error_reports += 1
        flashcard.save()


    if not description.strip():
        description = "<b>The user did not provide a description.</b>"
    else:
        description = 'The user provided this description: <b>' + description + '</b>'

    message = 'Hey there - a user reported a problem in the <b><u>'+ module +'</b></u> module, for <b>item ID '+ question_id +'</b>, which reads: <br /><br /> '+item+' <br /><br />'+ description +'<br/><br/> They categorized the bug as follows ' + categories[0]

    subject = 'ABA.Rocks - Problem Reported' + module + ', #' + item_id

    send_mail(subject,
        'Hey there - a user reported a problem on question ID '+ question_id +' with this description: ' + description + 'and the following categories were ' + categories[0],
        'alex@behaviorist.tech',
        ['alex@behaviorist.tech'],
        fail_silently=False,
        html_message=message,
    )

    return JsonResponse({
            'description' : description,
            'categories' : categories[0],
            'message' : message,
            'module' : module,
            'item_id' : item_id,
            'item' : item,
        })

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