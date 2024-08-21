"""
Ping hostnames on a hutch node and if unreachable add them to inactive_hostnames.csv
"""

from async_pinger import ping_all_hosts

if __name__ == "__main__":

    ping_all_hosts('inactive_hostnames.csv')

    # TO_DO: test code, remove later
    f1 = open("inactive_hostnames.csv", 'r+')
    lines = f1.readline().split(', ')
    print("\nSuccessfully pinged more devices. The number of inactive devices is now %d." % len(lines))
