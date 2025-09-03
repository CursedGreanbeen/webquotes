from django import forms


class AddQuoteForm(forms.Form):
    quote_text = forms.CharField()
    quote_source = forms.CharField()
    quote_author = forms.CharField()
    quote_weight = forms.IntegerField()
