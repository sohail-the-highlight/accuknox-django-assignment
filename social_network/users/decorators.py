from functools import wraps
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import available_attrs

def rate_limit(key, rate, method='POST', block=True):
    """
    Rate limit decorator based on Django's cache.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # Generate a unique cache key based on the request and the rate limiting key
            cache_key = f'{key}:{request.user.id if request.user.is_authenticated else request.META["REMOTE_ADDR"]}'
            
            # Get the current count from the cache or initialize it to 0
            count = cache.get(cache_key, 0)

            # Check if the count has exceeded the rate limit
            if count >= rate:
                if block:
                    # Optionally, you can raise a validation error or return a response
                    raise ValidationError('Rate limit exceeded')
                else:
                    return JsonResponse({'error': 'Rate limit exceeded'}, status=429)

            # Increment the count and set it back in the cache
            cache.set(cache_key, count + 1, timeout=60)  # Assuming a timeout of 60 seconds

            # Call the actual view function
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
