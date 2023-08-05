from django_filters import rest_framework as filters

from unicef_sharepoint.models import SharePointLibrary


class SharePointLibraryFilter(filters.FilterSet):

    class Meta:
        model = SharePointLibrary
        fields = {
            'site': ['exact', 'in'],
            'active': ['exact', ],
        }
