from django.views import View

# THIRD PARTY
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny


class RootApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response({
            'user': {
                'persons': reverse('persons:person:person-list', request=request,
                                   format=format, current_app='person'),
                'attributes': reverse('persons:person:attribute-list', request=request,
                                      format=format, current_app='person'),
                'validations': reverse('persons:person:validation-list', request=request,
                                       format=format, current_app='person'),
            },
            'debate': {
                'categories': reverse('debates:debate:category-list', request=request,
                                      format=format, current_app='debate'),
                'topics': reverse('debates:debate:topic-list', request=request,
                                  format=format, current_app='debate'),
                'access-groups': reverse('debates:debate:access_group-list', request=request,
                                         format=format, current_app='debate'),
                'access-members': reverse('debates:debate:access_member-list', request=request,
                                          format=format, current_app='debate'),
            },
        })
