from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import ArchiveForm, PatrimoineForm, FichierPlanForm
from .models import Archivist, Archive, Fichier_plan, Patrimoine


@login_required(login_url='main_app:login_client')
def dashboard(request):
    user = request.user
    list_archiviste = Archivist.objects.exclude(user=user)
    nom_page = "tableau de bord"

    archive_ancien = Archive.objects.filter(patrimoine__annee_construction__lte=2019)[5:]
    archive_nouveau = Archive.objects.filter(patrimoine__annee_construction__gte=2020)[5:]
    m_archive = Archive.objects.filter(archiviste=Archivist.objects.get(user=user))

    context = {
        'user': user, 'nom_page': nom_page,
        'list_archiviste': list_archiviste,
        'archive_ancien': archive_ancien,
        'archive_nouveau': archive_nouveau,
        'm_archive': m_archive
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='main_app:login_client')
def register_archive(request):

    error = {}
    context = {
        'error': error,
        'user': request.user,
    }

    if request.method == 'POST':
        formArchive = ArchiveForm(request.POST)
        formPat = PatrimoineForm(request.POST, request.FILES)
        formFichier = FichierPlanForm(request.POST, request.FILES)

        if formArchive.errors:
            error.update(formArchive.errors)
        if formPat.errors:
            error.update(formPat.errors)
        if formFichier.errors:
            error.update(formFichier.errors)

        if len(error) == 0:
            formPat.save()
            patrimoine = Patrimoine.objects.order_by('-pk').first()

            archive = Archive.objects.create(
                titre=formArchive.cleaned_data.get("titre"),
                archiviste=Archivist.objects.get(user=request.user),
                historique=formArchive.cleaned_data.get("historique"),
                patrimoine=patrimoine
            )
            archive.save()

            for fichier in formFichier.cleaned_data.get("fichier"):
                plan = Fichier_plan.objects.create(
                    patrimoine=patrimoine,
                    fichier=fichier,
                )
                plan.save()

                #return HttpResponse("tout est oky")
            return redirect("main_app:archive_detail", pk=archive.pk)

        else:

            context = {
                'user': request.user,
                'formArchive': formArchive,
                'formPat': formPat,
                'formFichier': formFichier,
                'error': error
            }
            #return HttpResponse("error")
    else:
        formArchive = ArchiveForm()
        formPat = PatrimoineForm()
        formFichier = FichierPlanForm()

        context = {
            'user': request.user,
            'formArchive': formArchive,
            'formPat': formPat,
            'formFichier': formFichier,
        }

    return render(request, 'register_archive.html', context)


@login_required(login_url='main_app:login_client')
def delete_archive(request, pk):
    user = request.user
    archive_ = Archive.objects.get(pk=pk)
    patrimoine_ = archive_.patrimoine
    fichiers_ = Fichier_plan.objects.filter(patrimoine=patrimoine_)
    try:
        archive_.delete()
        patrimoine_.delete()
        fichiers_.delete()
    except Exception as e:
        return HttpResponse(str(e))

    return redirect("archive_app:show_archive")


def edit_archive(request, pk):
    archive_ = Archive.objects.get(pk=pk)
    patrimoine_ = archive_.patrimoine
    fichiers_ = Fichier_plan.objects.filter(patrimoine=patrimoine_)

    error = {}
    if request.method == 'POST':
        formArchive = ArchiveForm(request.POST)
        formPat = PatrimoineForm(request.POST, request.FILES, instance=patrimoine_)
        formFichier = FichierPlanForm(request.POST, request.FILES)

        if formArchive.errors:
            error.update(formArchive.errors)
        if formPat.errors:
            error.update(formPat.errors)
        if formFichier.errors:
            error.update(formFichier.errors)

        if len(error) == 0:
            formPat.save()
            patrimoine = Patrimoine.objects.order_by('-pk').first()

            archive = Archive.objects.update(
                titre=formArchive.cleaned_data.get("titre"),
                archiviste=Archivist.objects.get(user=request.user),
                historique=formArchive.cleaned_data.get("historique"),
                patrimoine=patrimoine
            )
            archive.save()

            for fichier in formFichier.cleaned_data.get("fichier"):
                plan = Fichier_plan.objects.update(
                    patrimoine=patrimoine,
                    fichier=fichier,
                )
                plan.save()

                # return HttpResponse("tout est oky")
            return redirect("archive_app:show_archive")

        else:

            context = {
                'user': request.user,
                'formArchive': formArchive,
                'formPat': formPat,
                'formFichier': formFichier,
                'error': error,
                'archive': archive_,
                'patrimoine': patrimoine_,
                'fichiers': fichiers_
            }
            # return HttpResponse("error")
    else:
        formArchive = ArchiveForm()
        formPat = PatrimoineForm()
        formFichier = FichierPlanForm()

        context = {
            'user': request.user,
            'formArchive': formArchive,
            'formPat': formPat,
            'formFichier': formFichier,
            'archive': archive_,
            'patrimoine': patrimoine_,
            'fichiers': fichiers_
        }

    return render(request, 'edit_archive.html', context)


@login_required(login_url='main_app:login_client')
def show_archive(request):
    user = request.user
    archives = Archive.objects.all()

    context = {
        'user': user,
        'archives': archives
    }

    return render(request, 'show_all_archive.html', context)
