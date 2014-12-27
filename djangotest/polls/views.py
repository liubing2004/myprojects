from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from polls.models import Question, Choice
from django.views.decorators.csrf import csrf_exempt 


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

@csrf_exempt
def payment_return(request):
    print request
    return render(request, 'polls/index.html', {})

@csrf_exempt
def payment_cancel(request):
    print request
    return render(request, 'polls/index.html', {})     

def paypal(request):
    print request
    return render(request, 'polls/index.html', {})   
    
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import time
def view_that_asks_for_money(request):

    # What you want the button to do.
    invoice = str(int(round(time.time() * 1000)))
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10.00",
        "item_name": "test item",
        "invoice": "invoice-"+invoice,
        #"notify_url": "http://127.0.0.1" + reverse('paypal-ipn'),
        "notify_url": "http://127.0.0.1/polls/paypal/",
        "return_url": "http://127.0.0.1/polls/payment_return/",
        "return": "http://127.0.0.1/polls/payment_return?invoice="+invoice,
        "cancel_return": "http://127.0.0.1/polls/payment_cancel/",
        #"rm":2,
        "custom":"invoice="+invoice,

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "polls/payment.html", context)
