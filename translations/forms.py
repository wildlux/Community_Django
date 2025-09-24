from django import forms

class UploadPOForm(forms.Form):
    po_file = forms.FileField(label='Carica file .po')