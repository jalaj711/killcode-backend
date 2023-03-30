from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response

from knox.models import AuthToken
from knox.serializers import UserSerializer

from .models import Team, TeamMember
from .serializers import TeamSerializer

import hashlib

from django.db.utils import IntegrityError


# Only admin should be able to create a new user
@permission_classes(
    [
        AllowAny,
    ]
)
class TeamRegister(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        if (
            request.data.get("name", "") != "" and
            type(request.data.get("members", "")) == list and
            len(request.data.get("members")) >= 2 and
            len(request.data.get("members")) <= 4
        ):
            try:
                member_fields = ["name", "phone_number", "email"]
                members = []
                team = Team.objects.create(
                    name=request.data.get("name", ""), points=0)
                for i in request.data.get("members"):
                    for j in member_fields:
                        if j not in i:
                            raise ValueError("All fields were not provided")
                    member = TeamMember(name=i["name"], phone_number=i["phone_number"], email=i["email"],
                                        team=team, username=hashlib.md5(i["email"].encode()).hexdigest())
                    members.append(member)
                TeamMember.objects.bulk_create(members)
            except IntegrityError:
                return Response({
                    "success": False,
                    "message": "Team name already used."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Not all member fields provided"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {
                    "team": TeamSerializer(team).data,
                    "success": True,
                }
            )
        return Response({
            "success": False,
            "message": "Incorrect parameters"}, status=status.HTTP_400_BAD_REQUEST
        )

# @permission_classes([IsAdminUser])
# class get_all(generics.GenericAPIView):
#     serializer_class = UserSerializer
#     def get(self, request, *args, **kwargs):
#         user = User.objects.all().distinct()
#         page = self.paginate_queryset(user)
#         serialized = self.serializer_class(
#             page, context={'request': request}, many=True)
#         return self.get_paginated_response(serialized.data)


@permission_classes(
    [
        AllowAny,
    ]
)
class Login(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = dict(request.data)
        if (
            # (data.get("email") and
            #  data.get("email_verified") and
            #  data.get("family_name") and
            #  data.get("given_name") and
            #  data.get("name") and
            #  data.get("picture"))
                True is None):
            return Response('Not authenticated', status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = TeamMember.objects.get(email=data.get("email"))
            except TeamMember.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'This email id is not registered with us'
                }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                "success": True,
                "token": AuthToken.objects.create(user)[1]
            })
