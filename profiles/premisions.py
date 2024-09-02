from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomerToken

class CustomerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            token_obj = CustomerToken.objects.get(key=token)
        except CustomerToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return (token_obj.customer, None)
