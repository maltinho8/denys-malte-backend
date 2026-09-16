from django.shortcuts import render
from django.views.generic import DetailView, ListView
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import CarTypeChoices, Manufacture, ProductionStatusChoices
from .serializers import ManufactureSerializer


# ---------------------------------------------------------------------------
# Django Views
# Für normale HTML-Seiten mit Templates
# ---------------------------------------------------------------------------

# Function-Based View:
# HTML-Seite, wenn man die Logik komplett selbst schreiben möchte
def manufacture_list_view(request):
    manufactures = Manufacture.objects.all()

    context = {
        "manufactures": manufactures,
    }

    return render(request, "manufacture-list.html", context=context)


# ListView:
# HTML-Seite für eine Liste, wenn Django die Standardlogik übernehmen soll
class ManufactureListView(ListView):
    model = Manufacture
    template_name = "manufacture-list.html"
    context_object_name = "manufactures"


# DetailView:
# HTML-Seite für ein einzelnes Objekt, z. B. /manufactures/5/
class ManufactureDetailView(DetailView):
    model = Manufacture
    template_name = "manufacture-detail.html"
    context_object_name = "manufacture"


# ---------------------------------------------------------------------------
# Django REST Framework
# Für API-Endpunkte, die JSON zurückgeben
# ---------------------------------------------------------------------------

# Function-Based API View:
# Einfache, manuelle API-View für einzelne Endpunkte
@api_view(["GET"])
def manufacture_list_api_view(request):
    manufactures = Manufacture.objects.all()
    serializer = ManufactureSerializer(manufactures, many=True)

    return Response(serializer.data, status=200)


# APIView:
# API mit mehr Kontrolle; HTTP-Methoden wie GET und POST werden selbst definiert
class ManufactureAPIView(APIView):
    def get(self, request):
        manufactures = Manufacture.objects.all()
        serializer = ManufactureSerializer(manufactures, many=True)

        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = ManufactureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)


# GenericAPIView + Mixin:
# Für Standard-API-Funktionen, wenn DRF einen Teil der Logik übernehmen soll
class ManufactureGenericListAPIView(
    generics.GenericAPIView,
    ListModelMixin,
):
    queryset = Manufacture.objects.all()
    serializer_class = ManufactureSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# ModelViewSet:
# Für komplette CRUD-APIs; DRF stellt GET, POST, PUT, PATCH und DELETE bereit

# Aktuell wird diese View genutzt, um alle CRUD-Operationen für Manufacture bereitzustellen.
# View ist explizit an eine URL gebunden, die im Router definiert wird.
class ManufactureViewSet(ModelViewSet):
    queryset = Manufacture.objects.all()
    serializer_class = ManufactureSerializer

    def get_queryset(self):
        # Initial queryset: Das gesamte Manufacture-Objekt wird abgerufen, bevor Filter angewendet werden.
        queryset = Manufacture.objects.all()

        # Hier bilde ich die erlaubten Werte für die Filterung ab.
        allowed_production_status_values = ProductionStatusChoices.values
        allowed_car_type_values = CarTypeChoices.values

        # Parameter aus den Query-Parametern abrufen
        # Das bedeutet, dass wir die Filterung nur anwenden, wenn entsprechende Query-Parameter vorhanden sind.
        production_status = self.request.query_params.get("production_status")
        car_type = self.request.query_params.get("car_type")


        # Falls ein Filterparameter vorhanden ist, wende die Filterung an.
        # Filterung basierend auf den Query-Parametern anwenden
        # Bei Fehlern in den Filterparametern wird eine ValidationError ausgelöst.
        if production_status:
            if production_status not in allowed_production_status_values:
                raise ValidationError("Invalid production status value.")
            queryset = queryset.filter(production_status=production_status)
        if car_type:
            if car_type not in allowed_car_type_values:
                raise ValidationError("Invalid car type value.")
            queryset = queryset.filter(car_type=car_type)
        return queryset
