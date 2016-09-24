# from django.shortcuts import render
#
# # Create your views here.
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse
#
#
# from .models import Question, Choice
#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#
# def vote(request, question_id):
#     p = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = p.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/detail.html', {
#             'question': p,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
#

import json
import random

from django.shortcuts import get_object_or_404, render, Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from polls.models import *
from django.views.decorators.csrf import csrf_exempt

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
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

def training(request):
    return render(request, 'polls/training.html')

@csrf_exempt
def startguess(request):
    if request.method == 'GET':
        Number.objects.all().delete()
        newNumber = Number.objects.create()
        return HttpResponse(json.dumps([newNumber.id, random.randrange(newNumber.min, newNumber.max)]))
    else:
        return Http404('')

@csrf_exempt
def guess(request):
    if request.method == 'POST':
        number = Number.objects.get(id=request.POST.get('number_id'))
        last_number = int(request.POST.get('last_number'))
        if request.POST.get('response') == 'big':
            number.max = last_number - 1
        else:
            number.min = last_number + 1
        if number.max < number.min:
            return HttpResponse(json.dumps(['bad']))
        number.save()
        #print number
        if number.max == number.min:
            return HttpResponse(json.dumps([number.min]))
        else:
            return HttpResponse(json.dumps([random.randrange(number.min, number.max)]))
    else:
        return Http404('')
