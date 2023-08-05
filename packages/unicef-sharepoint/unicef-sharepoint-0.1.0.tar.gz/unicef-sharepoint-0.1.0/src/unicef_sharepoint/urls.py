from rest_framework import routers

from unicef_sharepoint.views import (
    FileSharePointViewSet,
    ItemSharePointCamlViewSet,
    ItemSharePointViewSet,
    SharePointLibraryViewSet,
    SharePointSiteViewSet,
    SharePointTenantViewSet,
)

app_name = 'unicef_sharepoint'

router = routers.DefaultRouter()

router.register(r'tenants', SharePointTenantViewSet, basename='sharepoint-tenant')
router.register(r'sites', SharePointSiteViewSet, basename='sharepoint-site')
router.register(r'libraries', SharePointLibraryViewSet, basename='sharepoint-library')
router.register(r'sharepoint/(?P<tenant>[\w\-]+)/(?P<site>[\w\-]+)/(?P<folder>[\w|\W]+)/files',
                FileSharePointViewSet, basename='sharepoint-files')
router.register(r'sharepoint/(?P<tenant>[\w\-]+)/(?P<site>[\w\-]+)/(?P<folder>[\w|\W]+)',
                ItemSharePointViewSet, basename='sharepoint')
router.register(r'sharepoint-caml/(?P<tenant>[\w\-]+)/(?P<site>[\w\-]+)/(?P<folder>[\w|\W]+)',
                ItemSharePointCamlViewSet, basename='sharepoint-caml')

urlpatterns = router.urls
