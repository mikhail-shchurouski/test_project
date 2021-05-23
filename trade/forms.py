from django import forms


class SearchForm(forms.Form):
    contract_id = forms.IntegerField()

