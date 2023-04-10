

# This is file is designed to show examples of how to use the python functions to connect to Rubrik Security Cloud
# and show examples of functions that have been built to execute RSC GraphQL queries to perform common Rubrik actions.
# This is designed as guidance system and can be customized to your individual needs.
# This is a community project and is not supported by Rubrik
# Author:  Jeremy Cathey (Rubrik Platform Solutions Architect)
# Date:  2023-04-10

from RSCFunctions import *

# ########### Start of RSC Authentication ##########
# Path to RSC Service Account JSON File
service_account_json_path = ''
# Connect to RSC using a JSON Service Account File
rsc = rsc_connect(service_account_json_path)
# ########### End of RSC Authentication ##########


# ########### Start Example ##########
# Live Mount Managed Volume via MV Name
# rsc_livemount_managedvolume(rsc['URI'], rsc['Headers'], "etstMV")
# ########### End Example ##########

# ########### Start Example ##########
# UnMount Managed Volume via MV Name
# rsc_unmount_managedvolume(rsc['URI'], rsc['Headers'], "etstMV")
# ########### End Example ##########

# ########### Start Example ##########
# Query for unregistered vSphere VMs and bulk register RBS (count <= 1000)
# rsc_register_vms_bulk(rsc['URI'], rsc['Headers'], 50)
# ########### End Example ##########

# ########### Start Example ##########
# Query vSphere VM and then register it's RBS
# rsc_register_vm(rsc['URI'], rsc['Headers'], "acme-bigvm-01")
# ########### End Example ##########

# ########### Start Example ##########
# threathunt_name = "PythonGraphQLTest4"
# cluster_uuid = "deec0cb8-183b-4e4e-9460-753aa23e2cc8"
# ioc_kind = "IOC_YARA"
# ioc_value = "import \"hash\"\n\nrule StringMatch : Example Rubrik {\n  meta:\n    description = \"string and regular expression matching\"\n\n  strings:\n    $wide_and_ascii_string = \"Borland\" wide ascii\n    $re = /state: (on|off)/\n\n  condition:\n   $re and $wide_and_ascii_string and filesize > 200KB\n}\n\nrule MatchByHash : Example Rubrik {\n  meta:\n    description = \"hash matching\"\n\n  condition:\n    filesize == 12345 and\n        hash.md5(0, filesize) == \"e30299799c4ece3b53f4a7b8897a35b6\"\n}\n"
# utc_start = "2023-04-01T05:00:00.000Z"
# utc_end = "2023-04-06T05:00:00.000Z"
# object_fids = ["03e01c93-1130-51f2-a327-05b3a8383c30", "6179bba1-0e1b-55b9-9315-d3b2e6c1d81a"]
# rsc_startThreatHunt(rsc['URI'], rsc['Headers'], threathunt_name, cluster_uuid, object_fids, ioc_kind, ioc_value, utc_start, utc_end)
# ########### End Example ##########
