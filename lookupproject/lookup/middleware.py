import logging
from django.db import IntegrityError, OperationalError
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class GlobalErrorHandlingMiddleware:
    """Custom middleware to handle database and other errors globally."""
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Process the request and handle exceptions globally."""
        try:
            response = self.get_response(request)
        except IntegrityError as e:
            logger.error(f"IntegrityError: {str(e)}")
            return JsonResponse({"error": "A database integrity issue occurred."}, status=500)
        except OperationalError as e:
            logger.error(f"OperationalError: {str(e)}")
            return JsonResponse({"error": "A database connection issue occurred."}, status=500)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)
        
        return response