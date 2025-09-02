from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quote, Source
from .forms import AddQuoteForm
import random


def index(request):
    quotes = list(Quote.objects.all())

    if not quotes:
        return render(request,
                      'quotes/index.html', context={'random': None})

    weights = [quote.weight for quote in quotes]
    random_quote = random.choices(quotes, weights=weights, k=1)[0]
    random_quote.views += 1
    random_quote.save()

    return render(request,
                  'quotes/index.html', context={'random_quote': random_quote})


def add_quote(request):
    add_quote_form = AddQuoteForm()

    if request.method == 'POST':
        add_quote_form = AddQuoteForm(request.POST)
        
        if add_quote_form.is_valid():
            normalized_source = add_quote_form.cleaned_data['quote_source'].strip().capitalize()
            quote_source = Source.objects.filter(name=normalized_source).first()
            quote_text = add_quote_form.cleaned_data['quote_text'].strip()
            quote_weight = add_quote_form.cleaned_data['quote_weight']

            if Quote.objects.filter(text=quote_text).exists():
                add_quote_form.add_error('quote_text', 'This quote already exists!')
                return render(request, 'quotes/add_quote.html', {'form': add_quote_form})

            if not quote_source:
                quote_source = Source.objects.create(name=normalized_source)
                new_quote = Quote.objects.create(
                    text=quote_text,
                    source=quote_source,
                    weight=quote_weight
                )
                messages.success(request, 'Quote added successfully!')
                return redirect('/')

            elif quote_source.quote_set.count() >= 3:
                add_quote_form.add_error('source', '3 quotes max per each source!')

            else:
                new_quote = Quote.objects.create(
                    text=quote_text,
                    source=quote_source,
                    weight=quote_weight
                )
                messages.success(request, 'Quote added successfully!')
                return redirect('/')

    return render(request, 'quotes/add_quote.html', {'form': add_quote_form})


def top_quotes(request):
    top = Quote.objects.order_by('-weight')[:10]
    return render(request,
                  'quotes/top_quotes.html', context={'quotes': top})


def vote(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        vote_type = request.POST.get('vote_type')

        quote = get_object_or_404(Quote, pk=quote_id)

        if vote_type == 'like':
            quote.likes += 1
        elif vote_type == 'dislike':
            quote.dislikes += 1

        quote.save()
        return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

    return JsonResponse({'error': 'Invalid request'}, status=400)
