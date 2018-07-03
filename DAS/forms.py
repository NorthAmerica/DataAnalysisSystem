from django import forms
from .models import Txt_Data

class TxtDataForm(forms.ModelForm):
	class Meta:
		model = Txt_Data
		fields = ('file',)