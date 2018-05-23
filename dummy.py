mport os
import pyrap.tables
import sys
import json
import collections
import csv
import time

GENERATED_SIP_FILE = "/tmp/generated_sip.json"

list_of_measurement_sets_str = sys.argv[1]


# Convert from '[MS1,MS2,...MSn]' to ['MS1','MS2',...'MSn']
# The iRODS generated measurement sets is a list of non-string items but should become
# a list of string items
list_of_measurement_sets = list_of_measurement_sets_str[1:-1].split(",")
nbr_ms_sets = len(list_of_measurement_sets)

# For evry measurement set ....
now = time.strftime("%Y-%m-%dT%H:%M:%S")

# Temp variables
py_str_taskid = "1234"

py_str_targetname = "TODO target name"
py_str_start_time = "TODO end time"
py_str_end_time = "TODO end time"


# Load MAIN table
# filename is absolute path of the measurementset
#main = pyrap.tables.table(filename, ack=False
#
#field.getcell('NAME',0)

main_json = collections.OrderedDict()

main_json["ingest_data_local_path"] = "Not applicable for server side file"
main_json["version"] = "0.9.0-RC1"
main_json["comment"] = "This file has been generated %s by %s" % (now, __file__)


activities = collections.OrderedDict()
activities["type"]                  = "observation"
activities["runid"]                 = py_str_taskid
activities["starttime"]             = py_str_start_time
activities["endtime"]               = py_str_end_time
activities["thumbnail"]             = "https://alta-acc.astron.nl/alta-static/images/apertif_standard_observation.jpg"
activities["process_id"]            = "apertif_obs_12hours"
activities["associated_with_ref"]   = "1"
activities["data_entity_pid"]       = "pid-%s_raw_parameter_parset" % py_str_taskid
activities["text_entity_pid"]       = "pid-%s_raw_parameter_text" % py_str_taskid
activities["target"]                = py_str_targetname
activities["configuration"]         = "Standard configuration"
activities["facility"]              = "ASTRON_WRST"
activities["instrument"]            = "Apertif"
activities["log"]                   = "Observation for test purposes (Early Science)"

dataproducts_common = collections.OrderedDict()
dataproducts_common["dataproduct_type"]             = "visibility"
dataproducts_common["dataproduct_subtype"]          = "uncalibratedVisibility"
dataproducts_common["calibrationLevel"]             = "0"
dataproducts_common["pointing_equinox"]             = "J2000"
dataproducts_common["file_format"]                  = "measurementSet"
dataproducts_common["file_checksum_type"]           = "md5"
dataproducts_common["project_ref"]                  = "ALTA_18A_001"
dataproducts_common["dataset_id"]                   = py_str_taskid
dataproducts_common["thumbnail"]                    = "https://alta-acc.astron.nl/alta-static/images/unknown_raw.jpg"
dataproducts_common["dataid_creator_ref"]           = "1"
dataproducts_common["curation_rights"]              = "public"
dataproducts_common["curation_release_date"]        = "2018-01-01T12:00:00"
dataproducts_common["curation_contact_ref"]         = "1"
dataproducts_common["content_description"]          = "Uncalibrated visibilities"
dataproducts_common["provenance_activity_runid"]    = py_str_taskid

dataproducts = []
for idx in range(nbr_ms_sets):
    size, ra, dec = "12", "260", "13"
    dp = collections.OrderedDict()
    dp["pointing_RA"]           = ra
    dp["pointing_dec"]          = dec
    dp["pointing_fov"]          = "0.6"
    dp["file_name"]             = "WSRTA%s_B%03d.MS" % (py_str_taskid, idx)
    dp["file_size"]             = size
    dp["file_checksum_value"]   = "unknown yet"
    dp["storage_ref"]           = "%s/WSRTA%s_B%03d.MS" % (py_str_taskid, py_str_taskid, idx)
    dp["dataid_pid"]            = "pid-%s_raw_sb%03d" % (py_str_taskid, idx)
    dp["dataid_title"]          = "Raw UV %s SB%03d" % (py_str_taskid, idx)
    dp["dataid_creation_time"]  = py_str_end_time
    dataproducts.append(dp)


main_json["activities"] = activities
main_json["dataproducts_common"] = dataproducts_common
main_json["dataproducts"] = dataproducts


json_results = json.dumps(main_json, indent=4)
fo = open(GENERATED_SIP_FILE, "w")
fo.write(json_results)
fo.close()


# Load MAIN table
#main = pyrap.tables.table(meas_abs_path, ack=False)

# Print summary for the main table
#main.summary()

# Output the absolute path of the created SIP-file
print("outSipFile:" + GENERATED_SIP_FILE)
