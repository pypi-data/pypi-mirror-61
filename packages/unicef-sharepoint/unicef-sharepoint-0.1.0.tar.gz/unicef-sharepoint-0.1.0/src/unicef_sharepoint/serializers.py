from django.conf import settings
from office365.sharepoint.helpers.utils import to_camel
from rest_framework import serializers
from rest_framework.reverse import reverse

from unicef_sharepoint.models import SharePointLibrary, SharePointSite, SharePointTenant


class SharePointPropertyField(serializers.ReadOnlyField):
    """tries to get attribute from the object or properties"""

    def get_attribute(self, instance):
        camel_case = to_camel(self.source)
        if getattr(instance, 'properties') and camel_case in instance.properties:
            return instance.properties[camel_case]
        return super().get_attribute(instance)


class SharePointPropertyManyField(serializers.ReadOnlyField):
    """tries to get attribute from the object or properties"""

    def get_attribute(self, instance):
        camel_case = to_camel(self.source)
        if getattr(instance, 'properties') and camel_case in instance.properties:
            values = instance.properties[camel_case]
            if values:
                values = values.replace('; ', ';').split(';')
            return values
        return super().get_attribute(instance)


class UpperSharePointPropertyField(serializers.ReadOnlyField):

    def get_attribute(self, instance):
        upper_case = self.source.upper()
        if getattr(instance, 'properties') and upper_case in instance.properties:
            return instance.properties[upper_case]
        return super().get_attribute(instance)


class SharePointTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharePointTenant
        exclude = ('username', 'password')


class SharePointSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharePointSite
        fields = '__all__'


class SharePointLibrarySerializer(serializers.ModelSerializer):
    site_name = serializers.ReadOnlyField(source='site.name')
    api_url = serializers.SerializerMethodField()

    def get_api_url(self, obj):
        reverse_url = reverse('unicef_sharepoint:sharepoint-list',
                              kwargs={'tenant': obj.site.tenant.name, 'site': obj.site.name, 'folder': obj.name})
        return settings.HOST + reverse_url

    class Meta:
        model = SharePointLibrary
        fields = ('name', 'site_name', 'active', 'library_url', 'api_url')


class SharePointItemSerializer(serializers.Serializer):

    id = UpperSharePointPropertyField()
    guid = UpperSharePointPropertyField()
    created = SharePointPropertyField()
    modified = SharePointPropertyField()
    title = SharePointPropertyField()
    url = SharePointPropertyField()
    resource_url = serializers.ReadOnlyField()
    download_url = serializers.SerializerMethodField()

    def get_download_url(self, obj):
        filename = obj.properties.get('Title', '')
        if filename:
            k = filename.rfind(".")
            filename = filename[:k] + "__ext__" + filename[k + 1:]
        relative_url = reverse('unicef_sharepoint:sharepoint-files-download', kwargs={
            'tenant': self.context['tenant'],
            'site': self.context['site'],
            'folder': self.context['folder'],
            'filename': filename
        })
        return f'{settings.HOST}{relative_url}'


class SharePointFileSerializer(serializers.Serializer):
    name = SharePointPropertyField()
    type_name = serializers.ReadOnlyField()
    url = serializers.ReadOnlyField()
    linking_uri = SharePointPropertyField()
    server_relative_url = SharePointPropertyField()
    unique_id = SharePointPropertyField()
    title = SharePointPropertyField()
    time_created = SharePointPropertyField()
    time_last_modified = SharePointPropertyField()

    def get_download_url(self, obj):
        relative_url = reverse('unicef_sharepoint:sharepoint-files-download', kwargs={
            'tenant': self.context['tenant'],
            'site': self.context['site'],
            'folder': self.context['folder'],
            'filename': obj.properties['Name'].split('.')[0]})
        return f'{settings.HOST}{relative_url}'
