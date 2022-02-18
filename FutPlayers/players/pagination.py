from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination

class PlayersPagination(PageNumberPagination):  
    page_size = 10
    
    def get_paginated_response(self, data):
        Items = self.get_page_size(self.request)
        paginator = self.django_paginator_class(data, Items)
        Page = self.get_page_number(self.request, paginator)
        totalItems = self.page.paginator.count
        totalPages = self.page.paginator.num_pages
        return OrderedDict([
            ('Items', Items),
            ('Page', Page),
            ('totalItems', totalItems),
            ('totalPages', totalPages),
            ('Players', data)
        ])