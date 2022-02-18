from django.urls import path
from .views import PlayerApiView, PlayersListView, PlayersTeamApiView

urlpatterns = [
    path("players/import", PlayerApiView.as_view()),
    path("players", PlayersListView.as_view()),
    path("team", PlayersTeamApiView),
]
