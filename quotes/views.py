from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quote, Source, Author
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
    try:
        add_quote_form = AddQuoteForm()

        if request.method == 'POST':
            add_quote_form = AddQuoteForm(request.POST)

            if add_quote_form.is_valid():
                normalized_source = add_quote_form.cleaned_data['quote_source'].strip()
                normalized_author = add_quote_form.cleaned_data['quote_author'].strip()
                quote_weight = add_quote_form.cleaned_data['quote_weight']
                quote_text = add_quote_form.cleaned_data['quote_text'].strip()

                if not quote_text:
                    add_quote_form.add_error('quote_text', 'Quote cannot be empty!')
                    return render(request, 'quotes/add_quote.html', {'form': add_quote_form})

                elif Quote.objects.filter(text=quote_text).exists():
                    add_quote_form.add_error('quote_text', 'This quote already exists!')
                    return render(request, 'quotes/add_quote.html', {'form': AddQuoteForm()})

                quote_source = None
                if normalized_source:
                    quote_source = Source.objects.filter(name=normalized_source).first()
                    if not quote_source:
                        quote_source = Source.objects.create(name=normalized_source)

                    elif quote_source.quote_set.count() >= 3:
                        add_quote_form.add_error('quote_source', '3 quotes max per each source!')
                        return render(request, 'quotes/add_quote.html', {'form': add_quote_form})

                quote_author = None
                if normalized_author:
                    quote_author = Author.objects.filter(name=normalized_author).first()
                    if not quote_author:
                        quote_author = Author.objects.create(name=normalized_author)

                new_quote = Quote.objects.create(
                    text=quote_text,
                    source=quote_source,  # Может быть None
                    author=quote_author,  # Может быть None
                    weight=quote_weight
                )

                messages.success(request, 'Quote added successfully!')
                return redirect('/')

        return render(request, 'quotes/add_quote.html', {'form': add_quote_form})

    except Exception as e:
        messages.error(request, 'Error adding quote: ' + str(e))
        return render(request, 'quotes/add_quote.html', {'form': AddQuoteForm()})


def top_quotes(request):
    top = Quote.objects.order_by('-weight')[:10]
    return render(request,
                  'quotes/top_quotes.html', context={'quotes': top})


def vote(request):
    try:
        if request.method == 'POST':
            quote_id = request.POST.get('quote_id')
            vote_type = request.POST.get('vote_type')
            quote = get_object_or_404(Quote, pk=quote_id)
            voted_quotes = request.session.get('voted_quotes', [])

            if str(quote_id) in voted_quotes:
                return JsonResponse({'error': 'You have already voted!',
                                     'message': 'You have already voted!'})
            if vote_type == 'like':
                quote.likes += 1
            elif vote_type == 'dislike':
                quote.dislikes += 1
            quote.save()

            voted_quotes.append(str(quote_id))
            request.session['voted_quotes'] = voted_quotes
            request.session.save()

            return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

        return JsonResponse({'error': 'Invalid request'}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'Invalid request' + str(e)}, status=500)
