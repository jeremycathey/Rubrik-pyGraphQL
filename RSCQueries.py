

# This is file contains example Rubrik Security Cloud (RSC) GraphQL queries to perform common Rubrik actions.
# This is designed as guidance system and can be customized to your individual needs.
# This is a community project and is not supported by Rubrik
# Author:  Jeremy Cathey (Rubrik Platform Solutions Architect)
# Date:  2023-04-10

import json
import time
import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables):
    json_body = {
        "query": query,
        "variables": variables
    }
    # Run GraphQL Query to Gather information about a virtual machine
    rsc_query = requests.post(rsc_uri, json=json_body, headers=rsc_headers)
    j = rsc_query.json()
    print(j)

    return j


def RSC_FindManagedVolumes(rsc_uri, rsc_headers, mv_name):
    query = """
        query ManagedVolumes($first: Int, $sortOrder: SortOrder, $filter: [Filter!]) {
          managedVolumes(first: $first, sortOrder: $sortOrder, filter: $filter) {
            nodes {
              cluster {
                id
                name
              }
              host {
                name
                id
              }
              id
              liveMounts {
                count
                nodes {
                  id
                  name
                  numChannels
                  channels {
                    mountSpec {
                      mountDir
                    }
                    id
                    floatingIpAddress
                  }
                }
              }
            }
            count
          }
        }
    """
    variables = {
        "first": 10,
        "sortOrder": "ASC",
        "filter": [
            {
                "field": "NAME",
                "texts": mv_name
            }
        ]
    }

    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)

    return j


def RSC_FindManagedVolumeIDByName(rsc_uri, rsc_headers, mv_name):
    query = """
        query ManagedVolumes($first: Int, $sortOrder: SortOrder, $filter: [Filter!]) {
          managedVolumes(first: $first, sortOrder: $sortOrder, filter: $filter) {
            nodes {
              cluster {
                id
                name
              }
              host {
                name
                id
              }
              id
              liveMounts {
                count
                nodes {
                  id
                  name
                  numChannels
                  channels {
                    mountSpec {
                      mountDir
                    }
                    id
                    floatingIpAddress
                  }
                }
              }
            }
            count
          }
        }
    """
    variables = {
        "first": 10,
        "sortOrder": "ASC",
        "filter": [
            {
                "field": "NAME",
                "texts": mv_name
            }
        ]
    }

    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)

    mv_id = j['data']['managedVolumes']['nodes'][0]['id']
    return mv_id


def RSC_ManagedVolume(rsc_uri, rsc_headers, mv_id):
    query = """
    query ManagedVolume($fid: UUID!, $first: Int, $sortOrder: SortOrder) {
      managedVolume(fid: $fid) {
        id
        liveMounts(first: $first, sortOrder: $sortOrder) {
          count
          nodes {
            id
            channels {
              floatingIpAddress
              id
              mountPath
              mountSpec {
                mountDir
                node {
                  id
                  ipAddress
                }
              }
            }
            name
            numChannels
            physicalPath {
              fid
              name
              objectType
            }
            sourceSnapshot {
              id
              date
            }
            logicalPath {
              fid
              name
              objectType
            }
          }
        }
        newestSnapshot {
          id
          date
        }
      }
    }
    """
    variables = {
        "fid": mv_id,
        "first": 50,
        "sortOrder": "ASC"
    }

    # Run GraphQL Query to Gather information about Managed Volume (Pass MV ID in GraphQL Query Variable Section)
    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)

    return j


def RSC_Get_ManagedVolume_LatestSnapshotID(rsc_uri, rsc_headers, mv_id):
    query = """
    query ManagedVolume($fid: UUID!, $first: Int, $sortOrder: SortOrder) {
      managedVolume(fid: $fid) {
        id
        liveMounts(first: $first, sortOrder: $sortOrder) {
          count
          nodes {
            id
            channels {
              floatingIpAddress
              id
              mountPath
              mountSpec {
                mountDir
                node {
                  id
                  ipAddress
                }
              }
            }
            name
            numChannels
            physicalPath {
              fid
              name
              objectType
            }
            sourceSnapshot {
              id
              date
            }
            logicalPath {
              fid
              name
              objectType
            }
          }
        }
        newestSnapshot {
          id
          date
        }
      }
    }
    """
    variables = {
        "fid": mv_id,
        "first": 50,
        "sortOrder": "ASC"
    }

    # Run GraphQL Query to Gather information about Managed Volume (Pass MV ID in GraphQL Query Variable Section)
    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
    mv_snap_id = j['data']['managedVolume']['newestSnapshot']['id']

    return mv_snap_id


def RSC_Get_ManagedVolume_LiveMountCount(rsc_uri, rsc_headers, mv_id):
    query = """
    query ManagedVolume($fid: UUID!, $first: Int, $sortOrder: SortOrder) {
      managedVolume(fid: $fid) {
        id
        liveMounts(first: $first, sortOrder: $sortOrder) {
          count
          nodes {
            id
            channels {
              floatingIpAddress
              id
              mountPath
              mountSpec {
                mountDir
                node {
                  id
                  ipAddress
                }
              }
            }
            name
            numChannels
            physicalPath {
              fid
              name
              objectType
            }
            sourceSnapshot {
              id
              date
            }
            logicalPath {
              fid
              name
              objectType
            }
          }
        }
        newestSnapshot {
          id
          date
        }
      }
    }
    """
    variables = {
        "fid": mv_id,
        "first": 50,
        "sortOrder": "ASC"
    }

    # Run GraphQL Query to Gather information about Managed Volume (Pass MV ID in GraphQL Query Variable Section)
    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
    mv_lm_count = j['data']['managedVolume']['liveMounts']['count']

    return mv_lm_count


def RSC_ExportManagedVolumeSnapshot(rsc_uri, rsc_headers, mv_snap_id):
    query = """
      mutation ManagedVolumeLiveMountMutation(
        $input: ExportManagedVolumeSnapshotInput!
      ) {
        exportManagedVolumeSnapshot(input: $input) {
          id
        }
      }
    """
    variables = {
        "input": {
            "id": mv_snap_id,
            "params": {
                "shouldDownloadToLocal": True,
                "managedVolumeExportConfig": {
                    "shareType": "MANAGED_VOLUME_SHARE_TYPE_NFS",
                    "managedVolumePatchConfig": {}
                }
            }
        }
    }
    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
    time.sleep(30)

    return j


def RSC_Get_ManagedVolume_ChannelPaths(rsc_uri, rsc_headers, mv_id):
    query = """
    query ManagedVolume($fid: UUID!) {
      managedVolume(fid: $fid) {
        liveMounts {
          count
          nodes {
            id
            channels {
              mountSpec {
                mountDir
              }
              floatingIpAddress
            }
            numChannels
          }
        }
      }
    }
    """
    variables = {
        "fid": mv_id,
        "first": 50,
        "sortOrder": "ASC"
    }
    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
    mv_lm_count = j['data']['managedVolume']['liveMounts']['count']
    while mv_lm_count == 0:
        j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
        time.sleep(15)
        mv_lm_count = j['data']['managedVolume']['liveMounts']['count']

    mv_lm_channel_count = j['data']['managedVolume']['liveMounts']['nodes'][0]['numChannels']
    # Decrement mvLMChannelCount by one because channel array starts at 0 not 1
    channel_record = 0
    mv_channel_path_array = []
    mv_channel_ip_array = []
    while channel_record < mv_lm_channel_count:
        mv_channel_path_array.append(
            j['data']['managedVolume']['liveMounts']['nodes'][0]['channels'][channel_record]['mountSpec']['mountDir'])
        mv_channel_ip_array.append(
            j['data']['managedVolume']['liveMounts']['nodes'][0]['channels'][channel_record]['floatingIpAddress'])
        channel_record = channel_record + 1

    # Create array of Paths for Teradata host to Mount
    count = 0
    mount_path_array = []
    print("Managed Volume Successfully Mounted.")
    print("Managed Volume Channel Paths List:")
    while count < mv_lm_channel_count:
        path = "//" + mv_channel_ip_array[count] + mv_channel_path_array[count] + "/"
        mount_path_array.append(path)
        print(mount_path_array[count])
        count = count + 1

    return mount_path_array


def RSC_Get_ManagedVolume_LiveMountID(rsc_uri, rsc_headers, mv_id):
    query = """
    query ManagedVolume($fid: UUID!) {
      managedVolume(fid: $fid) {
        liveMounts {
          count
          nodes {
            id
            channels {
              mountSpec {
                mountDir
              }
              floatingIpAddress
            }
            numChannels
          }
        }
      }
    }
    """
    variables = {
        "fid": mv_id,
        "first": 50,
        "sortOrder": "ASC"
    }
    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
    mv_live_mount_id = j['data']['managedVolume']['liveMounts']['nodes'][0]['id']

    return mv_live_mount_id


def RSC_DeleteManagedVolumeSnapshotExport(rsc_uri, rsc_headers, mv_live_mount_id):
    query = """
    mutation UnmountManagedVolumeLiveMountMutation(
        $input: DeleteManagedVolumeSnapshotExportInput!
      ) {
        deleteManagedVolumeSnapshotExport(input: $input) {
          id
        }
      }
    """
    variables = {
        "input": {
            "id": mv_live_mount_id
        }
    }
    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
    print("Managed Volume unMounting...")

    return j


def RSC_Get_vSphere_VM_ID(rsc_uri, rsc_headers, vm_name):
    query = """
    query VSphereVMsListQuery($first: Int!, $after: String, $filter: [Filter!]!, $isMultitenancyEnabled: Boolean = false, $sortBy: HierarchySortByField, $sortOrder: SortOrder, $isDuplicatedVmsIncluded: Boolean = true) {
      vSphereVmNewConnection(
        filter: $filter
        first: $first
        after: $after
        sortBy: $sortBy
        sortOrder: $sortOrder
      ) {
        edges {
          cursor
          node {
            id
            ...VSphereNameColumnFragment
            ...CdmClusterColumnFragment
            ...EffectiveSlaColumnFragment
            ...VSphereSlaAssignmentColumnFragment
            ...OrganizationsColumnFragment @include(if: $isMultitenancyEnabled)
            isRelic
            authorizedOperations
            primaryClusterLocation {
              id
              name
              __typename
            }
            logicalPath {
              fid
              name
              objectType
              __typename
            }
            slaPauseStatus
            snapshotDistribution {
              id
              onDemandCount
              retrievedCount
              scheduledCount
              totalCount
              __typename
            }
            reportWorkload {
              id
              archiveStorage
              physicalBytes
              __typename
            }
            vmwareToolsInstalled
            agentStatus {
              agentStatus
              __typename
            }
            duplicatedVms @include(if: $isDuplicatedVmsIncluded) {
              fid
              cluster {
                id
                name
                version
                status
                __typename
              }
              slaAssignment
              effectiveSlaDomain {
                ... on GlobalSlaReply {
                  id
                  name
                  isRetentionLockedSla
                  description
                  __typename
                }
                ... on ClusterSlaDomain {
                  id
                  fid
                  name
                  isRetentionLockedSla
                  cluster {
                    id
                    name
                    __typename
                  }
                  __typename
                }
                __typename
              }
              snapshotDistribution {
                id
                onDemandCount
                retrievedCount
                scheduledCount
                totalCount
                __typename
              }
              effectiveSlaSourceObject {
                fid
                objectType
                name
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        pageInfo {
          startCursor
          endCursor
          hasNextPage
          hasPreviousPage
          __typename
        }
        __typename
      }
    }
    
    fragment VSphereNameColumnFragment on HierarchyObject {
      id
      name
      ...HierarchyObjectTypeFragment
      __typename
    }
    
    fragment HierarchyObjectTypeFragment on HierarchyObject {
      objectType
      __typename
    }
    
    fragment EffectiveSlaColumnFragment on HierarchyObject {
      id
      effectiveSlaDomain {
        ...EffectiveSlaDomainFragment
        ... on GlobalSlaReply {
          description
          __typename
        }
        __typename
      }
      ... on CdmHierarchyObject {
        pendingSla {
          ...SLADomainFragment
          __typename
        }
        __typename
      }
      __typename
    }
    
    fragment EffectiveSlaDomainFragment on SlaDomain {
      id
      name
      ... on GlobalSlaReply {
        isRetentionLockedSla
        __typename
      }
      ... on ClusterSlaDomain {
        fid
        cluster {
          id
          name
          __typename
        }
        isRetentionLockedSla
        __typename
      }
      __typename
    }
    
    fragment SLADomainFragment on SlaDomain {
      id
      name
      ... on ClusterSlaDomain {
        fid
        cluster {
          id
          name
          __typename
        }
        __typename
      }
      __typename
    }
    
    fragment CdmClusterColumnFragment on CdmHierarchyObject {
      replicatedObjectCount
      cluster {
        id
        name
        version
        status
        __typename
      }
      __typename
    }
    
    fragment VSphereSlaAssignmentColumnFragment on HierarchyObject {
      effectiveSlaSourceObject {
        fid
        name
        objectType
        __typename
      }
      ...SlaAssignmentColumnFragment
      __typename
    }
    
    fragment SlaAssignmentColumnFragment on HierarchyObject {
      slaAssignment
      __typename
    }
    
    fragment OrganizationsColumnFragment on HierarchyObject {
      allOrgs {
        name
        __typename
      }
      __typename
    }

    """
    variables = {
        "isMultitenancyEnabled": True,
        "isDuplicatedVmsIncluded": True,
        "first": 50,
        "filter": [
            {
                "field": "IS_RELIC",
                "texts":
                    ["false"]
            },
            {
                "field": "IS_REPLICATED",
                "texts": ["false"]
            },
            {
                "field": "IS_ACTIVE",
                "texts": ["true"]
            },
            {
                "field": "NAME",
                "texts": [vm_name]
            },
            {
                "field": "IS_ACTIVE_AMONG_DUPLICATED_OBJECTS",
                "texts": ["true"]
            }
        ],
        "typeFilter": [
            "VmwareVirtualMachine",
            "VSphereComputeCluster",
            "VSphereDatacenter",
            "VSphereFolder",
            "VSphereHost",
            "VSphereTag",
            "VSphereTagCategory",
            "VSphereVCenter"
        ],
        "sortBy": "NAME",
        "sortOrder": "ASC"
    }

    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)

    vm_id = j['data']['vSphereVmNewConnection']['edges'][0]['node']['id']

    return vm_id


def RSC_Get_vSphere_VMs_Unregistered(rsc_uri, rsc_headers, vmcount):
    query = """
        query VSphereVmNewConnection($first: Int, $sortOrder: SortOrder) {
          vSphereVmNewConnection(first: $first, sortOrder: $sortOrder) {
            count
            nodes {
              id
              agentStatus {
                agentStatus
              }
            }
          }
        }
    """
    variables = {
        "first": vmcount,
        "sortOrder": "ASC"
    }
    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
    jcount = len(j['data']['vSphereVmNewConnection']['nodes'])
    count = 0
    vm_id_list = []
    vmAgentStatus = ""
    while count < jcount:
        if j['data']['vSphereVmNewConnection']['nodes'][count]['agentStatus'] is not None:
            vmAgentStatus = j['data']['vSphereVmNewConnection']['nodes'][count]['agentStatus']['agentStatus']

        if vmAgentStatus == "UNREGISTERED":
            vmID = j['data']['vSphereVmNewConnection']['nodes'][count]['id']
            vm_id_list.append(vmID)
            count = count + 1
        else:
            count = count + 1

    # print(*vm_list, sep="\n")
    # print(len(vm_id_list))

    if len(vm_id_list) == 0:
        print("There are no unregistered vSphere VMs")

    return vm_id_list


def RSC_vSphere_RegisterVMs_Bulk(rsc_uri, rsc_headers, vm_id_list):
    # Receive list of VMs and register them with RSC
    j = []
    count = 0
    jcount = len(vm_id_list)
    print("Registering VMs . . .")
    while count < jcount:
        query = """
             mutation RegisterRubrikBackupServiceMutation(
                $input: VsphereVmRegisterAgentInput!
              ) {
                vsphereVmRegisterAgent(input: $input) {
                  success
                }
            }
        """
        variables = {
            "input": {
                "id": vm_id_list[count]
            }
        }
        tmp = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)
        print(count)
        print(tmp)
        j.append(tmp)

        if tmp['data'] is not None:
            print("Successfully registered VM with ID: " + vm_id_list[count])
        else:
            print("Failure to register VM with ID: " + vm_id_list[count])
        count = count + 1

    # Returns array of error/success details
    return j


def RSC_vSphere_RegisterVM(rsc_uri, rsc_headers, vm_id):
    query = """
         mutation RegisterRubrikBackupServiceMutation(
            $input: VsphereVmRegisterAgentInput!
          ) {
            vsphereVmRegisterAgent(input: $input) {
              success
            }
        }
    """
    variables = {
        "input": {
            "id": vm_id
        }
    }
    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)

    if j['data'] is not None:
        print("Successfully registered VM with ID: " + vm_id)
    else:
        print("Failure to register VM with ID: " + vm_id)

    return j


def RSC_startThreatHunt(rsc_uri, rsc_headers, threathunt_name, cluster_uuid, object_fids, ioc_kind, ioc_value, utc_start, utc_end):
    query = """
    mutation StartThreatHuntMutation($input: StartThreatHuntInput!) {
        startThreatHunt(input: $input) {
          huntId
          isSyncSuccessful
        }
      }
    """
    variables = {
            "input":
                {
                    "clusterUuid": cluster_uuid,
                    "indicatorsOfCompromise":
                        [
                            {
                                "iocKind": ioc_kind,
                                "iocValue": ioc_value
                            }
                        ],
                    "objectFids": object_fids,
                    "fileScanCriteria":
                        {"fileSizeLimits":
                            {
                                "maximumSizeInBytes": 5000000},
                            "pathFilter":
                                {
                                    "includes": ["**"], ""
                                                        "excludes": "null",
                                    "exceptions": "null"
                                }
                        },
                    "maxMatchesPerSnapshot": 100,
                    "name": threathunt_name,
                    "shouldTrustFilesystemTimeInfo": True,
                    "snapshotScanLimit":
                        {
                            "maxSnapshotsPerObject": 10,
                            "startTime": utc_start,
                            "endTime": utc_end
                        }
                }
        }

    j = RSC_execute_graph_call(rsc_uri, rsc_headers, query, variables)

    return j

