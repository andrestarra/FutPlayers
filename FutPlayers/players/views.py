from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view
from .models import Player
from .serializers import PlayerSerializer, PlayerSerializerList, PlayersTeamSerializer
from .pagination import PlayersPagination

class PlayerApiView(views.APIView):

    def post(self, request):
        # Get JSON
        data = request.data['data']
        # Get DB data
        players = Player.objects.all()
        # Convert players into a list
        list_players = [player for player in players]
        # Serialize data
        serializer = PlayerSerializer(instance= list_players, data= data, many= True)

        # validate and save
        if serializer.is_valid():
            serializer.save()
            payload = {
                'code': status.HTTP_200_OK,
                'message': 'Ok',
                'data': serializer.data,
                'success': True
            }
        else:
            payload = {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad',
                'data': serializer.errors,
                'success': False
            }

        return Response(payload, status=status.HTTP_200_OK)

class PlayersListView(generics.ListAPIView):
    serializer_class = PlayerSerializerList
    queryset = Player.objects.all()
    pagination_class = PlayersPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def list(self, request):
        order = self.request.query_params['order'] if 'order' in self.request.query_params else None
        if not order or order == 'asc':
            queryset = Player.objects.order_by('name')
        elif order == 'desc':
            queryset = Player.objects.order_by('-name')
        else:
            queryset = Player.objects.none()
        self.object_list = self.filter_queryset(queryset)
        queryset =  self.object_list
        serializer_data = PlayerSerializerList(queryset, many= True)
        page = self.paginate_queryset(serializer_data.data)
        if page is not None:
            data = self.get_paginated_response(page)
        return Response(data, status=status.HTTP_200_OK)

@api_view(["POST"])
def PlayersTeamApiView(request):
    players = Player.objects.filter(team= request.data["Name"])
    serializer = PlayersTeamSerializer(players, many= True)
    if players:
        payload = {
            'code': status.HTTP_200_OK if serializer.data else status.HTTP_400_BAD_REQUEST,
            'totalItems': len(serializer.data) if serializer.data else 0,
            'Players': serializer.data if serializer else None,
            'success': True if serializer.data else False
        }
    else:
        payload = {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad',
            'data': ["There is no data"],
            'success': False
        }
    return Response(payload, status=payload['code'])
