'''
    Gets a data dump from netconfig of all hostnames in the database. Applies filters 
    from Google spreadsheet 
    (https://docs.google.com/spreadsheets/d/1opCKXzz78LQk2uB_hAAgOEGlbFLrlMm6X118zeh_AeA/edit?gid=389932230#gid=389932230) 
    and outputs hostnames to a csv file that will be used to ping devices across the network.

    NOTE: Some fields from netconfig, such as 'DHCP parameters' and 'Puppet Classes', 
    have been omitted. They are not used in the Google spreadsheet filters and do not 
    currently appear in the DoE IoT Asset Inventory template.
'''

import os
import re
import pandas as pd
from async_pinger import ping_all_hosts


if __name__ == "__main__":

    # Get the netconfig data dump and format it into a dictionary for pandas dataframe.
    os.system("netconfig search '*' > netconfig_data_dump.txt")

    # dictionary for pandas dataframe ingestion
    data_dump_dict = {'hostname': [], 'subnet': [], 'cnames': [], 'aliases': [], 'ethernet_address': [
    ], 'ip': [], 'contact': [], 'pc_number': [], 'location': [], 'description': []}

    # temporary container for each device's data
    device_dict = {'hostname': '', 'subnet': '', 'cnames': '', 'aliases': '', 'ethernet_address': '',
                   'ip': '', 'contact': '', 'pc_number': '', 'location': '', 'description': ''}

    file1 = open('netconfig_data_dump.txt', 'r')
    Lines = file1.readlines()

    for i, line in enumerate(Lines):

        if (not re.match('[\n]', line)) and (not re.match('^[\t]', line)) and (not re.match('^Found', line)):

            # found a new hostname, append the previous device's data to data_dump_dict
            for key, value in device_dict.items():
                data_dump_dict[key].append(value)

            device_dict = {key: '' for key in device_dict}

            head, sep, tail = line.partition(':')
            device_dict['hostname'] = head.strip()

        elif re.match(r'^[\t]', line):
            head, sep, tail = line.partition(':')
            head = head.strip()
            tail = tail.strip()

            # if a value already has single quotes, remove them
            if re.match(r'^\'.*\'$', tail):
                tail = tail[1:-1]

            # note that single quotes are applied to str(tail) for cases where the value of tail has commas
            if head == 'subnet':
                device_dict['subnet'] = str(tail)
            elif head == 'cnames':
                device_dict['cnames'] = "\'" + str(tail) + "\'"
            elif head == 'aliases':
                device_dict['aliases'] = "\'" + str(tail) + "\'"
            elif head == 'Ethernet Address':
                device_dict['ethernet_address'] = str(tail)
            elif head == 'IP':
                device_dict['ip'] = str(tail)
            elif head == 'Contact':
                device_dict['contact'] = "\'" + str(tail) + "\'"
            elif head == 'PC Number':
                device_dict['pc_number'] = "\'" + str(tail) + "\'"
            elif head == 'Location':
                device_dict['location'] = "\'" + str(tail) + "\'"
            elif head == 'Description':
                device_dict['description'] = "\'" + str(tail) + "\'"

    # Create pandas dataframe and apply filters from google sheets.
    df = pd.DataFrame(data_dump_dict)

    # filter out rows with empty strings in hostname column
    df = df.iloc[1:]

    # filter the 'ip' column
    df = df[~df["ip"].str.contains(
        "\d+\.\d+\.(?:40|164|57|152|156|40|67|26|59|27|24|23|25|21|22)\.\d+")]

    # filter the 'description' column
    df = df[~df['description'].str.contains(
        '(?i)i[\s-]*p[\s-]*m[\s-]*i|(?i)Sup[\s]*ermicr?o|(?i)Oracle|(?i)dell|(?i)digi|(?i)Cia[\s]*ra|ANA Interface|(?i)daq|(?i)moxa|(?i)laptop|(?i)mac[\s]*book|(?i)console|(?i)mforce|ICS|Lap[\s]top|Framework 13 Ryzen')]

    # output entire dataframe to csv file
    df.to_csv("filtered_all.csv", index=False)

    # Ping all filtered hostnames and get a list of inactive devices.
    filtered_hostnames = df.iloc[:, 0].tolist()  # get filtered hostnames

    with open('filtered_hostnames.csv', 'w+') as f:
        for device in filtered_hostnames[:len(filtered_hostnames) - 2]:
            f.write("\'%s\', " % device.strip())

        # removes the pesky extra comma at the end of the text file
        last_host = filtered_hostnames[len(filtered_hostnames) - 1]
        f.write("\'%s\'" % last_host.strip())

    ping_all_hosts('filtered_hostnames.csv')
