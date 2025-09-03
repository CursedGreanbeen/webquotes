from django import forms


class AddQuoteForm(forms.Form):
    quote_text = forms.CharField(widget=forms.Textarea, max_length=1000)
    quote_source = forms.CharField(max_length=250, required=False)
    quote_author = forms.CharField(max_length=100, required=False)
    quote_weight = forms.IntegerField(min_value=1, max_value=10)
