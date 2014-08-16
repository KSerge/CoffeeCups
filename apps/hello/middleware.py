from .models import IncomingRequest


class IncomingRequestsMiddleware(object):
    def process_request(self, request):
        incoming_request = IncomingRequest(path=request.get_full_path())
        incoming_request.save()