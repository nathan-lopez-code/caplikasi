from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from archive_app.models import Archive, Patrimoine, Fichier_plan
from .utils import compare_password
from .forms import Login_form, Client_register_form
from .models import Client, Archivist
from django.contrib.auth import get_user_model
from archive_app.forms import Reseach_form


@login_required(login_url='main_app:login_client')
def home(request):
    client = Client.objects.filter(user=request.user)
    archivist = Archivist.objects.filter(user=request.user)
    recent_archives = Archive.objects.all()[:5]
    search_form = Reseach_form()


    is_archiviste = False
    if client:
        user = client
    else:
        user = archivist
        is_archiviste = True

    return render(
        request, 'home.html', context={
            'user': user, 'is_archiviste': is_archiviste,
            'recent_archives': recent_archives,
            'search_form': search_form,
            'page_ac': "Accueil"
        })


@login_required(login_url='main_app:login_client')
def contact(request):
    client = Client.objects.filter(user=request.user)
    archivist = Archivist.objects.filter(user=request.user)

    is_archiviste = False
    if client:
        user = client
    else:
        user = archivist
        is_archiviste = True

    context = {
        'user': user,
        'is_archiviste': is_archiviste,
        'page_ac': "Contact"
    }

    return render(request, 'contact.html', context)


def login_client(request):
    if request.method == 'POST':
        form = Login_form(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            try:

                user = get_user_model().objects.get(username=username, password=password)
            except:
                user = None

            if user is not None:
                login(request, user)
                if Client.objects.filter(user=user).exists():
                    # diriger vers la page d'accueil
                    return redirect("main_app:home")
                else:
                    # diriger vers l'administration
                    return redirect("archive_app:dashboard")
            else:
                errors = "Aucun utilisateur ne correspond aux coordonnées fournies"
        else:
            errors = form.errors
    else:
        errors = False
        form = Login_form()

    return render(request, 'login_simple.html', context={"form": form, "errors": errors})


def register_client(request):
    if request.method == 'POST':
        form = Client_register_form(request.POST)
        if form.is_valid():
            username = request.POST['username']
            nom = request.POST['nom']
            email = request.POST['email']
            password = request.POST['password']
            confirmation = request.POST['confirm_password']

            if compare_password(password, confirmation):

                try:
                    user_existing = get_user_model().objects.get(username=username)
                except:
                    user_existing = None

                # verifier si le nom d'utilisateur et l'email existe
                if user_existing:
                    errors = "username ou email deja pris , essayez un autre"
                else:

                    try:

                        # creation d'un nouvel utilisateur
                        user = get_user_model().objects.create_user(
                            username=username, first_name=nom, email=email, password=password)
                        user.save()
                    except:
                        user = None
                    # connection a la table client
                    cl = Client.objects.create(user=user)
                    cl.save()
                    user = authenticate(request, username=username, password=password, email=email)
                    if user is not None:
                        login(request, user)
                        return redirect("main_app:home")
                    else:
                        errors = "Un utilisateur existe déjà avec ces coordonnées"

            else:
                errors = "Les deux mots de passe ne correspondent pas"

        else:
            errors = form.errors
    else:
        errors = False
        form = Client_register_form()

    return render(request, 'register_simple.html', context={"form": form, 'errors': errors})


@login_required(login_url='main_app:login_client')
def archive_detail(request, pk):
    client = Client.objects.filter(user=request.user)
    archivist = Archivist.objects.filter(user=request.user)
    archive = Archive.objects.get(pk=pk)
    is_archiviste = False

    fichiers_plan = Fichier_plan.objects.filter(patrimoine=archive.patrimoine)

    if client:
        user = client
    else:
        user = archivist
        is_archiviste = True

    context = {
        'user': request.user, 'is_archiviste': is_archiviste,
        'archive': archive, 'fichiers_plan': fichiers_plan
    }

    return render(request, 'detail_archive.html', context)


def logout_client(request):
    logout(request)
    return redirect("main_app:home")


@login_required(login_url='main_app:login_client')
def tout_archive(request):
    client = Client.objects.filter(user=request.user)
    archivist = Archivist.objects.filter(user=request.user)

    archives_a = Archive.objects.filter(patrimoine__type_construction="Ancienement")
    archives_n = Archive.objects.filter(patrimoine__type_construction="Nouvellement")

    is_archiviste = False
    search_form = Reseach_form()

    if client:
        user = client
    else:
        user = archivist
        is_archiviste = True

    context = {
        'user': user,
        'archive_a': archives_a,
        'archive_n': archives_n,
        'is_archiviste': is_archiviste,
        'search_form': search_form,
        'page_ac': "Archive"

    }

    return render(request, "all_archive.html", context)


@login_required(login_url='main_app:login_client')
def projets(request):
    client = Client.objects.filter(user=request.user)
    archivist = Archivist.objects.filter(user=request.user)
    archives_a = Archive.objects.filter(patrimoine__type_construction="Ancienement")
    archives_n = Archive.objects.filter(patrimoine__type_construction="Nouvellement")
    is_archiviste = False
    search_form = Reseach_form()

    if client:
        user = client
    else:
        user = archivist
        is_archiviste = True

    context = {
        'user': user,
        'is_archiviste': is_archiviste,
        'search_form': search_form,
        'page_ac': "Projet",
        'archives_a': archives_a,
        'archives_n': archives_n,

    }

    return render(request, "projets.html", context)


@login_required(login_url='main_app:login_client')
def recherche_archive(request):
    TTC = "toutes les communes"
    TT = "Tout type"
    NC = "Nouvellement construit"
    AC = "Ancienement construit"

    commune = request.GET.get('commune')
    titre = request.GET.get('titre')
    type = request.GET.get('type')

    query_result = {}

    if type == TT and commune != TTC:
        query_patrimoine = Patrimoine.objects.filter(commune=commune)
    elif type == NC and commune != TTC:
        query_patrimoine = Patrimoine.objects.filter(commune=commune, annee_construction__gt=2020)
    elif type == AC and commune != TTC:
        query_patrimoine = Patrimoine.objects.filter(commune=commune, annee_construction__lte=2019)
    elif type == AC and commune == TTC:
        query_patrimoine = Patrimoine.objects.filter(annee_construction__lte=2019)
    elif type == NC and commune == TTC:
        query_patrimoine = Patrimoine.objects.filter(annee_construction__gt=2000)
    else:
        query_patrimoine = Patrimoine.objects.all()

    if titre:
        archives = Archive.objects.filter(titre__contains=titre)
    else:
        archives = Archive.objects.all()

    archives = archives.filter(patrimoine__in=query_patrimoine)

    return render(request, 'search_resultat.html', context={'archives': archives})
