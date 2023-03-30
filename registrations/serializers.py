from rest_framework.serializers import ModelSerializer
from .models import TeamMember, Team

class TeamMemberSerializer(ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ("id", "name", "email")

class TeamSerializer(ModelSerializer):
    teammember_set = TeamMemberSerializer(many=True)
    class Meta:
        model = Team
        fields = ('id', 'name', 'points', 'teammember_set')
