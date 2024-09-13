# from djoser.views import UserViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import UserCreateSerializer

# class CustomUserCreateView(UserViewSet):
#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         print('response', response)
#         # Controlla se l'utente è stato creato correttamente
#         if response.status_code == status.HTTP_201_CREATED:
#             user = self.get_object()
#             refresh = RefreshToken.for_user(user)
#             tokens = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }

#     
#             return Response({
#                 'user': response.data,
#                 'tokens': tokens
#             }, status=status.HTTP_201_CREATED)

#         return response
        