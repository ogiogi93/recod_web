from django import forms

from service_api.models.disciplines import Game
from service_api.models.teams import Team


class UpsertTeamForm(forms.ModelForm):
    error_css_class = 'has-error'
    name = forms.CharField(max_length=50,
                           label='チーム名',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'}),
                           required=True,
                           error_messages={
                               'required': 'そのチーム名は既に使用されています'
                           })
    description = forms.CharField(required=False, label='チーム紹介文',
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}),
                                  error_messages={
                                      'required': 'チーム紹介文を入力して下さい'})

    game = forms.ModelChoiceField(queryset=Game.get_enabled_games(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control'}),
                                  label='活動ゲーム')
    image = forms.ImageField(required=False, label='チーム画像',
                             widget=forms.FileInput(attrs={
                                 'class': 'form-control'}
                             ))

    class Meta:
        model = Team
        fields = ('name', 'description', 'game', 'image')
