from django.shortcuts import render
import os
import glob
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
            # Lösche Inhalt des Media Ordners
            media_folder = settings.MEDIA_ROOT
            files = glob.glob(os.path.join(media_folder, '*'))
            try:
                for file in files:
                    os.remove(file)
            except Exception as e:
                print(f"Error: {e}")

            uploaded_file = request.FILES['uploaded_file']
            
            # Datei speichern
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  # Absoluter Pfad der Datei

            # Debugging: Ausgabe des Dateipfads
            print(f"File saved at: {file_path}")

            # Übergabe der URL und des absoluten Pfads an das Template
            return render(request, 'BichselApp/index.html', {
                'file_url': file_url,
                'file_path': file_path  # Absoluter Pfad zur Verwendung in der image_processing-View
            })
        else:
            # Fehlermeldung, falls keine Datei hochgeladen wurde
            return render(request, 'BichselApp/index.html', {'message': 'Keine Datei ausgewählt'})
    return render(request, 'BichselApp/index.html')

def image_processing(request):
    # Den Dateipfad und die Date-URL aus der Anfrage erhalten
    file_url = request.GET.get('file_url')
    file_path = request.GET.get('file_path')

    # Debugging: Prüfe, ob die Werte korrekt empfangen wurden
    print(f"File URL: {file_url}")
    print(f"File Path: {file_path}")

    # Überprüfe, ob der Pfad existiert
    if not file_path or not os.path.exists(file_path):
        return render(request, 'BichselApp/index.html', {'message': 'Datei nicht gefunden'})

    # Antwort von ask_bichsel erhalten
    response = ask_bichsel(file_path)

    return render(request, 'BichselApp/index.html', {'file_path': file_path, 'file_url': file_url, 'answer': response})

