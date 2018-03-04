from django import forms

from service_api.models.tournaments import Tournament, Participate


class ParticipateTournamentForm(forms.ModelForm):
    tournament = forms.ModelChoiceField(queryset=Tournament.objects.filter(is_active=True),
                                        widget=forms.Select(attrs={
                                            'class': 'form-control'}),
                                        label='大会')

    class Meta:
        model = Participate
        fields = ('tournament',)
