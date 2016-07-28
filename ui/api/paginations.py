from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):
    """
    Django enables pagination to limit response size.
    This class makes the pages a lot larger so that in all normal cases
    everything should be displayed.
    """
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class BareLimitOffsetPagination(LimitOffsetPagination):
    def get_previous_link(self):
        if self.offset <= 0:
            return None
        if self.offset - self.limit <= 0:
            return 0
        return self.offset - self.limit

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('limit', self.limit),
            ('results', data)
        ]))

    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None
        return self.offset + self.limit

