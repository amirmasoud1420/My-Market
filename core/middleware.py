import time
import logging


class TimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        logger = logging.getLogger('project.developers')
        start_time = time.time()
        response = self.get_response(request)
        logger.debug(f'view process Time : {time.time() - start_time}')



        # Code to be executed for each request/response after
        # the view is called.

        return response
