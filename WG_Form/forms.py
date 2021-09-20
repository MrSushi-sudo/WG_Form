from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import widgets


class NewFileInput(widgets.FileInput):
    template_name = 'new_file_input.html'


class FileForm(forms.Form):
    file = forms.FileField(widget=NewFileInput, validators=[FileExtensionValidator(allowed_extensions=['txt'])])

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = ""
