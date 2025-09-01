from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.http import require_POST
from .models import Quote, Source
from .forms import AddQuoteForm
import random


def index(request):
    quotes = list(Quote.objects.all())
    random_quote = random.choice(quotes)
    return render(request,
                  'quotes/index.html', context={'random': random_quote})


def add_quote(request, q_text, q_source, q_weight):
    add_quote_form = AddQuoteForm()
    source = q_source.strip().capitalize()
    if source.quote_set.count() >= 3:
        raise ValidationError('Из одного источника не более 3 цитат!')
    else:
        new_quote = Quote.objects.create(text=q_text, source=source, weight=q_weight)
    return render(request, 'add_quote.html', {"form": add_quote_form})


def top_quotes(request):
    # quotes = list(Quote.objects.all())
    # quotes.sort(key=lambda x: x.likes, reverse=True)
    # top = quotes[:10]
    top = Quote.objects.order_by('-weight')[:10]
    return render(request, 'quotes/top_quotes.html', context={'quotes': top})


def vote(request, q_id, vote_type):
    quote = get_object_or_404(Quote, pk=q_id)
    if vote_type == 'like':
        quote.likes += 1
    elif vote_type == 'dislike':
        quote.dislikeslikes += 1
    quote.save()
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

