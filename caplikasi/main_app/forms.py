from django import forms


# formulaire pour la connexion
class Login_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Saissisez votre nom d'utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Saissisez votre mot de passe'}))


# formulaire d'enregistrement de nouveau utilisateur client
class Client_register_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Creez votre nom utilisateur unique'}))
    nom = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Saissez votre nom'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Saissisez votre email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Saissisez votre mot de passe'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez votre mot de passe'}))

