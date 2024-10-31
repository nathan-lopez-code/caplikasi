from django import forms
from .models import COMMUNE_LIKASI, ETAT, Patrimoine


COMMUNE_LIKASI_S = [
    ("toutes les communes", "Toutes les communes"),
    ("kikula", "Kikula"),
    ("Likasi", "Likasi"),
    ("Panda", "Panda"),
    ("Shituru", "Shituru"),
]

TYPE = [
    ("Tout type", "Tout type"),
    ("Nouvellement construit", "Nouvellement construit"),
    ("Ancienement construit", "Ancienement construit"),

]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ArchiveForm(forms.Form):
    titre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': "Saississez le titre de l'archive"}))
    historique = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': "Saissisez l'historique"}),
                                 required=False)


class FichierPlanForm(forms.Form):
    fichier = MultipleFileField()


class PatrimoineForm(forms.ModelForm):
    class Meta:
        model = Patrimoine
        fields = '__all__'
    numero = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    avenue = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    commune = forms.ChoiceField(choices=COMMUNE_LIKASI, widget=forms.Select(attrs={'class': 'form-control'}))
    annee_construction = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    architecte = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Nom de l'architecte")
    etat_conservation = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ETAT)
    affectation_actuel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    observation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    image = forms.FileField(
        label='image du batiment',
        #attrs={'class': 'my-file-input'}
    )

    #name="area" class="form-select" aria-label="Area" id="chooseCategory" onchange="this.form.click()"


# formulaire de recherche
class Reseach_form(forms.Form):
    commune = forms.ChoiceField(choices=COMMUNE_LIKASI_S, widget=forms.Select(
        attrs={
            'class': 'form-select',
            'name': 'erea',
            'aria-label': "Area",
            'id': "chooseCategory",
            'onchange': "this.form.click()"
        }), required=False)
    type = forms.ChoiceField(choices=TYPE, widget=forms.Select(
        attrs={
            'class': 'form-select',
            'name': "price",
            'aria-label': "Tout type",
            'id':"chooseCategory",
            'onchange': "this.form.click()"
        }), required=False)
    titre = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': "address",
            'name': "address",
            'class': "searchText",
            'placeholder': "Saissisez le titre de l'archive"
        }), required=False)
