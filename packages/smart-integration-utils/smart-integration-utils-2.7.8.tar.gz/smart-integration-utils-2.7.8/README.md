# utils for integrations

## install
Install using `pip`...

    pip install smart-integration-utils


# settings
```python

#add to settings.py
DASHBOARD_URL = "https://9tnvnh6ri0.execute-api.eu-central-1.amazonaws.com/dashboard/"
BUCKET_NAME = 'zappa-fullbucket'
EXECUTE_TOKEN = '<token for dashboard app>'
```
## usage
```python
# fields
from integration_utils.fields import UTF8JSONField
from django.db import models

class Entity(models.Model):
    ...
    config = UTF8JSONField() # postresql jsonb field for correct ascii characters


# mixins
from integration_utils.mixins import CredentialMixin
from rest_framework.views import APIView

class Test(CredentialMixin, APIView):
    def get(self, request):
        user_info = self.get_user_info(request) # get smart user info if Auth token in headers
        admin = self.get_check_admin(request) # return admin id or False if not smart admin
        credential = self.get_credential(request, Credential) # Credential is auth model in our servers, return cred
                                                              # model or raise PermissionDenied exception 
        

# serializers
from integration_utils.serialziers import GeneratorSerializer, CalculationDynamicFieldSerializer
# GeneratorSerializer instance of https://github.com/bzdvdn/drf-dynamicfieldserializer

class DataSerializer(GeneratorSerialzier):
    ...

d = DataSerilizer(queryset)
d.generator # return a generator of your data
d.data # return list of your data

class CalcDataSerializer(CalculationDynamicFieldSerializer): # for calculation data if integration have calculation step
    ...

# views
from integration_utils.veiws import BaseCredentialModelViewSet, BaseReportListAPIView
from .models import Credential
from .serializers import CredentialSerializer

class CredentialViewSet(BaseCredentialModelViewSet): # mro CredentialMixin, ModelViewSet
    queryset = Credential.obejcts.all()
    serializer_class = CredentialSerializer


class EntityListAPIView(BaseReportListAPIView): 
    """return from GET qury a paginated result from your data by integration_id and date params (date_from=2020-01-20
        &date_to=2020-01-20)"""
    model = Entity
    serializer_class = EntitySerializer
    select_related_fields = ('contact', 'manager') # if needed select_related


# tools
from integration_utils.tools import chunk_of_generators

list_ = [i for i in range(1, 100000000)]
chunk_of_generators(iter(list_), 25000) # split your iterator/generator for 25000 items

from integration_utils.tools import delete_file

delete_file('<path to file>') # delete file from your disc

from integration_utils.tools import write_file

data = [{str(i): i} for i in range(1, 100000000)]
 # write tsv/csv file
write_file(filename='<path_to_file>', date=data, fieldsnames = None, delimiter='\t', extension='.tsv')


from integration_utils.tools import upload_to_s3

upload_to_s3(filename='<path_to_local_file>', folder='stats/') # filename - local file, folder - folder on s3 bucket

from integration_utils.tools import get_file_link

get_file_link(filename='filename', folder='stats/', suffix='.tsv') # get link to download file(not download from boto3)

from integration_utils.tools import chunk_by_items

data = [i for i in range(1, 100000000)]
chunk_by_items(data, 10000) # return generator for split your list by 10000


from integration_utils.tools import get_full_integrations

# return all integrations from comagic integration
integrations = get_full_integrations(platform='prod', sevice_code='comagic')


from copy import copy
from integration_utils.tools import check_entities_equal
from .models import Deal
db_deal = Deal.objects.first()
new_deal = copy(db_deal)
new_deal.name = '123'

check_entities_equal(db_deal=db_deal, new_deal=new_deal) # return True/False check to deals equals


from integration_utils.tools import chunk_by_parts

data = [i for i in range(1, 100000000)]
chunk_by_parts(data, 5) # return generator for split your list by 5 pars


from integration_uils.tools import delete_s3_file

delete_s3_file(filename='filename', folder='stats/', suffix='.tsv') # delete file from s3 bucket

from integration_utils.tools import encode, decode

credential_secure_password = '1qazxsw2'
encoded = encode(credential_secure_password) # encrypt secure data
decoded = decode(encoded) # decrypt secure data

# utils
from integration_utils.utils import parse_utm

url = 'https://test.io/?utm_source=google&utm_medium=cpc&utm_campaign=1'
utm = parse_utm(url) # return {'utm_source': 'google', 'utm_medium': 'cpc', 'utm_campaign': '1'}
```