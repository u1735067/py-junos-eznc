import pdb

from pprint import pprint as pp 

from exampleutils import *
from jnpr.eznc import Netconf as Junos
from jnpr.eznc.resources.srx import ApplicationSet
from jnpr.eznc.utils import ConfigUtils
from jnpr.eznc.exception import *

from lxml.builder import E 
from lxml import etree

login = dict(user='jeremy', host='vsrx_cyan', password='jeremy1')
jdev = Junos(**login)
jdev.open()

jdev.ez( cu=ConfigUtils )
jdev.ez( apps=ApplicationSet )

r = jdev.ez.apps['WWSS-A2A-WEB-INTRA']

# print the contents of the object
pp(r)

# >>> pp(r)
# NAME: ApplicationSet: WWSS-A2A-WEB-INTRA
# HAS: {'_active': True,
#  '_exists': True,
#  'app_list': ['TCP-9152',
#               'TCP-9153',
#               'TCP-9154',
#               'TCP-9155',
#               'TCP-9156',
#               'TCP-9159',
#               'TCP-9160',
#               'TCP-9161',
#               'TCP-9162',
#               'TCP-9169',
#               'TCP-9170',
#               'TCP-9171'],
#  'appset_list': []}
# SHOULD:{}

# now remove a few items from the app_list
# first make a copy of the existing list

r.copy('app_list')

# then remove a few
r['app_list'].remove("TCP-9162")
r['app_list'].remove("TCP-9155")

# maybe add some
r['app_list'].append("TCP-21")

# now write the resource
r.write()

# show the diff
print jdev.ez.cu.diff()

# [edit applications application-set WWSS-A2A-WEB-INTRA]
#      application TCP-9171 { ... }
# +    application TCP-21;
# -    application TCP-9155;
# -    application TCP-9162;

# you can rollback the changes:
# jdev.ez.cu.rollback()