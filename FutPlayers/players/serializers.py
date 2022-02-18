from dataclasses import fields
from rest_framework import serializers
from .models import Player

class PlayerSerializerList(serializers.Serializer):
    name = serializers.CharField()
    position = serializers.CharField()
    nation = serializers.CharField()
    team = serializers.CharField()

    class meta:
        model = Player
        fields = "__all__"
        
class PlayerListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        player_mapping = {player.name: player for player in instance}
        data_mapping = {item['name']: item for item in validated_data}
        
        # Perform creations and updates.
        ret = []
        for player_name, data in data_mapping.items():
            player = player_mapping.get(player_name, None)
            if player is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(player, data))
        
        # Perform deletions.
        for player_name, player in player_mapping.items():
            if player_name not in data_mapping:
                player.delete()
            
        return ret
        
class PlayerSerializer(serializers.ModelSerializer):
    # We need to identify elements in the list using their primary key,
    # so use a writable field here, rather than the default which would be read-only.
    name = serializers.CharField()
    
    class Meta:
        list_serializer_class = PlayerListSerializer
        model = Player
        fields = "__all__"
        
class PlayersTeamSerializer(serializers.Serializer):
    name = serializers.CharField()
    position = serializers.CharField()
    nation = serializers.CharField()
    
    class Meta:
        model = Player
        fields = "__all__"
