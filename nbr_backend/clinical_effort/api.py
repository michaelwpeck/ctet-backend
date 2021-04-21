from django.db.models import Q
from django.template.loader import get_template
from django.conf import settings

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

import json
import io
import hashlib

from clinical_effort.models import CTEffort, CycleTypes, PersonnelTypes, TrialArms, Cycles, Visits, Personnel, CRCVisit, NCVisit, DCVisit, GeneralVisit
from .serializers import CTEffortSerializer, CycleTypesSerializer, PersonnelTypesSerializer, TrialArmsSerializer, CyclesSerializer, VisitsSerializer, PersonnelSerializer, CRCVisitSerializer, NCVisitSerializer, DCVisitSerializer, GeneralVisitSerializer

from clinical_effort.actions.project import setup_project
from clinical_effort.actions.arms import add_arm
from clinical_effort.actions.cycles import add_cycle

# Clinical trial effort Viewset
class CTEffortViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = CTEffort.objects.all()
    serializer_class = CTEffortSerializer
    lookup_field = 'id'

    @action(detail=False, methods=['PUT'])
    def new(self, request, id=None):

        # Save project
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Call setup project action
        add_proj = setup_project(request.data, serializer.data['id'])

        # Retrieve new project
        project = CTEffort.objects.get(id=serializer.data['id'])
        p_serializer = self.serializer_class(project, many=False)

        return Response(p_serializer.data, status=200)


    @action(detail=True, methods=['GET'])
    def add_arm(self, request, id=None):

        # Create arm
        arm = add_arm(name='New Arm', proj_id=id)

        # Retrieve updated project
        project = CTEffort.objects.get(id=id)
        p_serializer = self.serializer_class(project, many=False)

        return Response(p_serializer.data, status=200)




# Cycle types Viewset
class CycleTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = CycleTypes.objects.all()
    serializer_class = CycleTypesSerializer
    lookup_field = 'id'


# Personnel types Viewset
class PersonnelTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = PersonnelTypes.objects.all()
    serializer_class = PersonnelTypesSerializer
    lookup_field = 'id'


# Clinical trial instance arms Viewset
class TrialArmsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = TrialArms.objects.all()
    serializer_class = TrialArmsSerializer
    lookup_field = 'id'

    @action(detail=False, methods=['GET'])
    def new_cycle(self, request, id=None):
        arm = self.queryset.filter(id=id)[0]
        add_cycle(type='custom', proj_id=arm.instance, arm_id=id)

        return Response('Worked', status=200)



# Clinical trial instance cycles Viewset
class CyclesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Cycles.objects.all()
    serializer_class = CyclesSerializer
    lookup_field = 'id'


# Clinical trial instance visits Viewset
class VisitsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Visits.objects.all()
    serializer_class = VisitsSerializer
    lookup_field = 'id'


# Personnel Viewset
class PersonnelViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    lookup_field = 'id'


# Clinical research coordinator visits Viewset
class CRCVisitViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = CRCVisit.objects.all()
    serializer_class = CRCVisitSerializer
    lookup_field = 'id'


# Nurse coordinator visits Viewset
class NCVisitViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = NCVisit.objects.all()
    serializer_class = NCVisitSerializer
    lookup_field = 'id'


# Data coordinator visits Viewset
class DCVisitViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = DCVisit.objects.all()
    serializer_class = DCVisitSerializer
    lookup_field = 'id'


# General visit Viewset
class GeneralVisitViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = GeneralVisit.objects.all()
    serializer_class = GeneralVisitSerializer
    lookup_field = 'id'
