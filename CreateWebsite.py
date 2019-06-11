# Create a Resource Group and Storage Account in Microsoft Azure
# Resource Groups are used to store and organize resources in Azure.
# Storage Accounts are used to store & share your data & files in different formats.
# Run this code from a python session on the Azure Cloud Shell.
# After the resource group and storage account are created, verify their existence from the Azure Portal (http://portal.azure.com)

### Install modules needed to create Azure VM from PowerShell or Bash console
'''
# importlib package must be installed for this script to work
# pip install importlib
# If modules become unstable during exercises, uninstall and then reinstall them.  
# You may also need to rename or move all files in the azure configuration folder /home/<USER>/.azure
# pip uninstall azure azure.cli azure.cli.core azure.mgmt azure.common azure.storage azure.storage.common azure.storage.blob azure.storage.file
pip install --user azure azure.cli azure.cli.core azure.mgmt azure.common azure.storage azure.storage.common azure.storage.blob azure.storage.file
pip list
python
'''

### This looping operation will install the modules not already configured.
import importlib, os, sys, datetime
packages = ['azure', 'azure.cli', 'azure.cli.core', 'azure.mgmt', 'azure.mgmt.storage', 'azure.common', 'azure.storage',  'azure.storage.common', 'azure.storage.blob', 'azure.storage.file']
for package in packages:
  try:
    module = importlib.__import__(package)
    print(package, ' package was imported.')
    globals()[package] = module
  except ImportError:
    cmd = 'pip install --user ' + package
    print('Please wait.  Package is being installed: ', package)
    os.system(cmd)
    module = importlib.__import__(package)
    print(package, ' package was imported.')

# These modules are used for authenticating to Azure, using resources and managing storage.  
# Install them if they are not already on the system: pip install --upgrade --user azure-common azure-mgmt azure-storage
import datetime, os, ftplib, xml.etree.ElementTree as ET
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.common import CloudStorageAccount
from azure.storage.file import FileService
from azure.storage.blob import PublicAccess
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import AppServicePlan, SkuDescription, Site, SiteAuthSettings

# Configure Clients for Managing Resources
resource_client = get_client_from_cli_profile(ResourceManagementClient)
storage_client = get_client_from_cli_profile(StorageManagementClient)
web_client = get_client_from_cli_profile(WebSiteManagementClient)

# Configure Variables
nameprefix = 'np' + (datetime.datetime.now()).strftime('%H%M%S')
resourcegroupname = nameprefix + 'rg'
storageaccountname = nameprefix + 'sa'
serverfarmname = nameprefix + 'sf'
websitename = nameprefix + 'web'
location = 'eastus'
sharename = '55264a'
profilefilename = websitename+'.xml'

# create a test file to be uploaded to your blob and file share
os.system('echo "<h1> This is my first Azure web-site. </h1>" > index.html')
filename = 'index.html'

# Create the Resource Group and Storage Account.  Use Azure Portal to examine their properties before deleting them.
resource_group_params = {'location':location}
resource_client.resource_groups.create_or_update(resourcegroupname, resource_group_params)
storageaccount = storage_client.storage_accounts.create(resourcegroupname, storageaccountname, {'location':location,'kind':'storage','sku':{'name':'standard_ragrs'}})
storageaccount.wait()

# Create Container and Share
sak = storage_client.storage_accounts.list_keys(resourcegroupname, storageaccountname)
storageaccountkey = sak.keys[0].value
cloudstorage_client =  CloudStorageAccount(storageaccountname,storageaccountkey)
blob_service = cloudstorage_client.create_block_blob_service()
blob_service.create_container(sharename,public_access=PublicAccess.Container)
file_service = FileService(account_name=storageaccountname, account_key=storageaccountkey)
file_service.create_share(sharename)

# Copy Setup Files to Container and Share
blob_service.create_blob_from_path(sharename,filename,filename,)
file_service.create_file_from_path(sharename,'',filename,filename,)

# Create an App Service Plan
service_plan_async_operation = web_client.app_service_plans.create_or_update(
    resourcegroupname,
    serverfarmname,
    AppServicePlan(
        app_service_plan_name=serverfarmname,location=location,
        sku=SkuDescription(
            name='F1',capacity=10,tier='Free'
        )
    )
)
service_plan = service_plan_async_operation.result()

# Create Web-Site
site_async_operation = web_client.web_apps.create_or_update(
    resourcegroupname,
    websitename,
    Site(
        location=location,
        server_farm_id=service_plan.id
    )
)
website = site_async_operation.result()
if website.state == 'Running': print("Website http://" +  website.default_host_name + " has deployed successfully.")
else: print("Website not deployed successfully.")

# View the new web-site before proceeding with the following steps. 
# Get Profile Information to Extract FTP Credentials
profile_list = list(web_client.web_apps.list_publishing_profile_xml_with_secrets(resourcegroupname,websitename))
publishsettingsfile = open(profilefilename,'w+')
for n in profile_list: 
    publishsettingsfile.write(str(n))

publishsettingsfile.close()
xml = ET.fromstring(profile_list[0])
for table in xml.iter('publishData'):
    for record in table:
        print(record.tag, record.text)

# Upload Files To Web-Site Using FTP
username = websitename
password = record.get('userPWD')
ftpserver = (record.get('publishUrl')).replace('ftp://w','w')
ftpserver = (ftpserver).replace('net/site/wwwroot','net')
ftp = ftplib.FTP(ftpserver)
ftp.connect()
ftp.login(username,password)
ftp.cwd('/site/wwwroot')
ftp.storbinary('STOR '+filename, open(filename,'rb'))
ftp.quit()

# Delete Resource Group.  Deleting a resource group will also deleted all objects in it.
# delete_async_operation = resource_client.resource_groups.delete(resourcegroupname)
# delete_async_operation.wait()


