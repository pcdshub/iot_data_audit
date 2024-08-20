#!/bin/bash


USER_PATH="${HOME}/git/iot_data_audit/iot_data_audit/"
CURR_SERVER="tst-console"

# check for valid kerebos tickets so user doesn't have to manually type in password when ssh-ing
if ! klist -s
then
    kinit
fi

echo -e "\nThis application generates an IoT Asset Inventory spreadsheet based on all \nvalid, ping-able devices on the network. Kerebos tickets have been activated \nto minimize typing in passwords to access hutch computers.\n"

# Start program on rhel7
ssh $CURR_SERVER "cd ${USER_PATH} && source /reg/g/pcds/engineering_tools/latest-released/scripts/pcds_conda && python3 filter_hostnames.py"

# Ping hostnames from inactive_hostnames.csv on every hutch node. If the device pings, 
# delete it from the list of inactive hostnames. The final list will contain all 
# inactive hostnames on the network.

declare -a SERVERS_ARR=("psbuild-rhel7" "psdev01" "kfe-console" "las-console" "lfe-console" "mec-control" "mfx-console" "rix-console" "tmo-console" "xcs-console" "xpp-control")

for ssh_host in ${SERVERS_ARR[@]}
do
    ssh $ssh_host "cd ${USER_PATH} && source /reg/g/pcds/engineering_tools/latest-released/scripts/pcds_conda && python3 find_inactive.py"
done

cd $USER_PATH
source /reg/g/pcds/engineering_tools/latest-released/scripts/pcds_conda
python3 write_to_spreadsheet.py