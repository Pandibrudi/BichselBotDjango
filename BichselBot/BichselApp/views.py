from django.shortcuts import render
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .bichsel_classifier import ask_bichsel

def index(request):
    return render(request, 'BichselApp/index.html')


def upload(request):
    if request.method == "POST":
        # Überprüfe, ob eine Datei hochgeladen wurde
        if 'uploaded_file' in request.FILES:
            uploaded_file = request.FILES['uploaded_file']
            
            # Datei speichern
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)
            
            return render(request, 'BichselApp/index.html', {'file_url': file_url})
        else:
            # Fehlermeldung, falls keine Datei hochgeladen wurde
            return HttpResponse("No file was uploaded.")
    return render(request, 'BichselApp/index.html')

def image_processing(request):
    # Den Dateipfad und die Date-URL aus der Anfrage erhalten
    file_url = request.GET.get('file_url')
    file_path = request.GET.get('file_path')  # Falls erforderlich

    # Debugging: Prüfe, ob die Werte korrekt empfangen wurden
    print(f"File URL: {file_url}")
    print(f"File Path: {file_path}")

    response = ask_bichsel()

    # Weiterverarbeitung des Bildes (optional)

    return render(request, 'BichselApp/index.html', {'file_url': file_url, 'file_path': file_path, 'answer' : response})

