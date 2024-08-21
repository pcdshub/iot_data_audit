# This module uses asyncIO to ping a list of hostnames.

import asyncio

inactive = []


async def ping(host):
    host = str(host)
    proc = await asyncio.create_subprocess_shell(
        f'ping {host} -c 3',
        stderr=asyncio.subprocess.DEVNULL,      # silence ping errors
        stdout=asyncio.subprocess.DEVNULL       # silence ping output
    )
    stdout, stderr = await proc.communicate()

    # If ping was unsuccessful, add to list of inactive devices.
    if proc.returncode:
        inactive.append(host)


def ping_all_hosts(filename):

    hostnames = []

    f1 = open(filename, 'r+')
    lines = f1.readline().split(', ')
    hostnames = [host.replace('\'', '') for host in lines]

    f1.close()

    loop = asyncio.get_event_loop()             # create an async loop
    tasks = []                                  # list to hold ping tasks

    for host in hostnames:
        task = ping(host)
        tasks.append(task)

    tasks = asyncio.gather(*tasks)              # assemble the tasks
    loop.run_until_complete(tasks)              # run tasks all at once

    # delete file contents to avoid writing duplicates
    open('inactive_hostnames.csv', 'w+').close()

    with open('inactive_hostnames.csv', 'w') as f2:
        for device in inactive[:len(inactive)-2]:
            f2.write("\'%s\', " % device.strip())

        # remove the pesky extra comma at the end of the text file
        last_host = inactive[len(inactive)-1]
        f2.write("\'%s\'" % last_host.strip())

    f2.close()
