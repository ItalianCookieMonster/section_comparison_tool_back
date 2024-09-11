from rest_framework.response import Response
from rest_framework import status

def format_validation_error(e):
    return Response({
        "message": "Validation failed: %s" % str(e),
        "errors": e.message_dict
    }, status=status.HTTP_400_BAD_REQUEST)

def format_unexpected_error(e):
    return Response({
        "message": "An unexpected error occurred: %s" % str(e),
        "errors": {"detail": str(e)}
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)