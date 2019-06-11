# Create a Resource Group and Storage Account in Microsoft Azure
# Resource Groups are used to store and organize resources in Azure.
# Storage Accounts are used to store & share your data & files in different formats.
# Run this code from a python session on the Azure Cloud Shell.
# After the resource group and storage account are created, verify their existence from the Azure Portal (http://portal.azure.com)

'''
pip install --user azure-mgmt azure-common azure-storage azure-storage-common azure-cli azure-cli-core
pip list
python
'''

'''

### This looping operation will install the modules not already configured.
# importlib package must be installed for this script to work   (pip install importlib)
import importlib, os, sys
packages = ['azure', 'azure.cli', 'azure.cli.core', 'azure.mgmt', 'azure.common', 'azure.storage', 'azure.storage.common', 'azure.storage.blob', 'azure.storage.file']
for package in packages:
  try:
    module = importlib.__import__(package)
    globals()[package] = module
  except ImportError:
    cmd = 'pip install --user ' + package
    os.system(cmd)
    module = importlib.__import__(package)

# These modules are used for authenticating to Azure, using resources and managing storage.  
# Install them if they are not already on the system: pip install --upgrade --user azure-common azure-mgmt azure-storage
import datetime, os
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.common import CloudStorageAccount
from azure.storage.file import FileService
from azure.storage.blob import PublicAccess

# Configure Clients for Managing Resources
resource_client = get_client_from_cli_profile(ResourceManagementClient)
storage_client = get_client_from_cli_profile(StorageManagementClient)

# Configure Variables
nameprefix = 'np' + (datetime.datetime.now()).strftime('%H%M%S')
resourcegroupname = nameprefix + 'rg'
storageaccountname = nameprefix + 'sa'
location = 'eastus'
sharename = '55264a'

# create a test file to be uploaded to your blob and file share
os.system('echo "This is a test." > test.txt')
filename = 'test.txt'

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

# Delete Resource Group.  Deleting a resource group will also deleted all objects in it.
# delete_async_operation = resource_client.resource_groups.delete(resourcegroupname)
# delete_async_operation.wait()


