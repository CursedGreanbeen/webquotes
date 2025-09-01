from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Quote, Source
from .forms import AddQuoteForm
import random


def index(request):
    quotes = list(Quote.objects.all())
    random_quote = random.choice(quotes)
    return render(request,
                  'quotes/index.html', context={'random': random_quote})


def add_quote(request):
    add_quote_form = AddQuoteForm()

    if request.method == 'POST':
        add_quote_form = AddQuoteForm(request.POST)
        if add_quote_form.is_valid():
            normalized_source = add_quote_form.quote_source.strip().capitalize()
            quote_source = Source.objects.filter(name=normalized_source).first()

            if not quote_source:
                quote_source = Source.objects.create(name=normalized_source)
                new_quote = Quote.objects.create(
                    text=add_quote_form.quote_text,
                    source=quote_source,
                    weight=add_quote_form.quote_weight
                )
                messages.success(request, 'Quote added successfully!')
                return redirect('index')

            elif quote_source.quote_set.count() >= 3:
                add_quote_form.add_error('source', '3 quotes max per each source!')

            else:
                new_quote = Quote.objects.create(
                    text=add_quote_form.quote_text,
                    source=quote_source,
                    weight=add_quote_form.quote_weight
                )
                messages.success(request, 'Quote added successfully!')
                return redirect('index')

    return render(request, 'quotes/add_quote.html', {'form': add_quote_form})


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

