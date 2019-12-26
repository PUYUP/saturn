from django.urls import path, include

from .views import RootApiView

from apps.person.api import routers as person_routers
from apps.debate.api import routers as debate_routers

urlpatterns = [
    path('', RootApiView.as_view(), name='api'),
    path('person/', include((person_routers, 'person'), namespace='persons')),
    path('debate/', include((debate_routers, 'debate'), namespace='debates')),
]
