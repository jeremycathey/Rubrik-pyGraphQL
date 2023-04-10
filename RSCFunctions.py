

# This is file contains example python functions to connect to Rubrik Security Cloud
# and execute RSC GraphQL queries to perform common Rubrik actions.
# This is designed as guidance system and can be customized to your individual needs.
# This is a community project and is not supported by Rubrik
# Author:  Jeremy Cathey (Rubrik Platform Solutions Architect)
# Date:  2023-04-10

from RSCQueries import *

import json
import time
import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)




def rsc_connect(json_path):
    # Setup token auth
    json_file = open(json_path)
    json_key = json.load(json_file)
    json_file.close()
    session_url = json_key['access_token_uri']
    payload = {
        "client_id": json_key['client_id'],
        "client_secret": json_key['client_secret'],
        "name": json_key['name']
    }
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain'
    }
    request = requests.post(session_url, json=payload, headers=headers, verify=False)
    del payload
    response_json = request.json()
    if 'access_token' not in response_json:
        print("Authentication failed!")
    access_token = response_json['access_token']

    rscConnect = dict();
    # Setup token auth for direct graphql queries external to the SDK.
    rscConnect['URL'] = session_url.rsplit("/", 1)[0]
    rscConnect['Token'] = access_token
    rscConnect['URI'] = session_url.rsplit("/", 1)[0] + '/graphql'
    rscConnect['Headers'] = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    print("Connected to RSC.")

    return rscConnect


def rsc_execute_graphql_query(rsc_uri, rsc_headers, query, variables):
    # Execute graphQL query based off of passed variables query and variables.
    response = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
    return response


def rsc_livemount_managedvolume(rsc_uri, rsc_headers, mv_name):
    # function call to use the managed volume name to retrieve the managed volume id
    mv_id = RSC_FindManagedVolumeIDByName(rsc_uri, rsc_headers, mv_name)
    # function call to use the managed volume id to retrieve the latest snapshot id
    snapshot_id = RSC_Get_ManagedVolume_LatestSnapshotID(rsc_uri, rsc_headers, mv_id)
    # function call to check if the managed volume is already live mounted
    RSC_Get_ManagedVolume_LiveMountCount(rsc_uri, rsc_headers, mv_id)
    # function call to live mount the managed volume
    RSC_ExportManagedVolumeSnapshot(rsc_uri, rsc_headers, snapshot_id)
    # function call to retrieve the managed volume channel paths
    RSC_Get_ManagedVolume_ChannelPaths(rsc_uri, rsc_headers, mv_id)
    # function call to retrieve the id of the live mounted managed volume
    mv_livemount_id = RSC_Get_ManagedVolume_LiveMountID(rsc_uri, rsc_headers, mv_id)
    return mv_livemount_id


def rsc_unmount_managedvolume(rsc_uri, rsc_headers, mv_name):
    # function call to use the managed volume name to retrieve the managed volume id
    mv_id = RSC_FindManagedVolumeIDByName(rsc_uri, rsc_headers, mv_name)
    # function call to retrieve the id of the live mounted managed volume
    mv_livemount_id = RSC_Get_ManagedVolume_LiveMountID(rsc_uri, rsc_headers, mv_id)
    # function call to unmount the live mounted managed volume
    mv_unmount = RSC_DeleteManagedVolumeSnapshotExport(rsc_uri, rsc_headers, mv_livemount_id)
    return mv_unmount


def rsc_register_vms_bulk(rsc_uri, rsc_headers, vmcount):
    # Get list of vSphere virtual machines that are unregistered
    vm_id_list = RSC_Get_vSphere_VMs_Unregistered(rsc_uri, rsc_headers, vmcount)
    # Pass list of vSphere virtual machines IDs to be registered
    response = RSC_vSphere_RegisterVMs_Bulk(rsc_uri, rsc_headers, vm_id_list)
    return response


def rsc_register_vm(rsc_uri, rsc_headers, vm_name):
    # Call function to get vSphere VM ID from the VM name
    vm_id = RSC_Get_vSphere_VM_ID(rsc_uri, rsc_headers, vm_name)
    # Call function to register vSphere virtual machine
    response = RSC_vSphere_RegisterVM(rsc_uri, rsc_headers, vm_id)
    return response


def rsc_startThreatHunt(rsc_uri, rsc_headers, threathunt_name, cluster_uuid, object_fids, ioc_kind, ioc_value, utc_start, utc_end):
    # pass variables and start a threat hunt
    response = RSC_startThreatHunt(rsc_uri, rsc_headers, threathunt_name, cluster_uuid, object_fids, ioc_kind, ioc_value, utc_start, utc_end)
    return response

