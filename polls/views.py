from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice


def index(request):
    question_list = Question.objects.order_by('-pub_date')[:5]
    # out = '\n'.join([q.question_text for q in question_list])
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': question_list
    }
    return render(request, 'polls/index.html', context)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist!")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return HttpResponse(render(request, 'polls/results.html', {'question':question}))


class ResultsView(generic.DetailView):
    model = Question
    template_name =  'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = question.choice_set.get(pk=request.POST['choice'])
        print(request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_msg': 'You did not select a choice.',
        })
    else:
        choice_id.votes += 1
        choice_id.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))