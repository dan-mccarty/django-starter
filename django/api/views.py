from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .authentication import AccountApiKeyAuthentication
from .permissions import HasApiScope


class OrdersView(APIView):
    authentication_classes = [
        AccountApiKeyAuthentication
    ]  # or include SessionAuthentication too
    permission_classes = [HasApiScope]
    required_scopes = ["orders:read"]

    def get(self, request):
        account = request.account
        # filter by account
        return Response({"account_id": account.id})
