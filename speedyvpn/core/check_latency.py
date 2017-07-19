from __future__ import print_function

from speedyvpn.core.Collector import Collector
from speedyvpn.utils.compat import sysencode

from os import path
from glob import glob
from multiprocessing.dummy import Pool
from subprocess import call, getoutput



__doc__ = ''' All in one for updating vpn files, pinging vpn, connecting to vpn with credentials file'''



def update_servers():
    """
    Step 1: [OPTIONAL] update the list of VPN servers to check.
    ===========================================================
    """
    args_pre_encoding = ['sudo', 'bash', 'update_servers.sh']
    args = [sysencode(i) for i in args_pre_encoding]
    call(args)


def threadPool():
    """
    Step 2: collect latencies and store them inside Collector.
    ==========================================================
     - & DO IT 300 TIMES AT ONCE
    """
    # for safety
    servers = get_servers()
    for i in Pool(300).imap(cycle, servers):
        pass


def get_servers():
    """
    Step 2a: match tcp servers in the US in ovpn folder.
    ====================================================
    """
    match = 'us'
    opvn_targets = glob('./OVPN/' + match + '*' + 'tcp*') #<--What is this?
    assert len(opvn_targets) > 1
    return opvn_targets

def cycle(ovpn):
    """
    Step 2b: Read opvn file, ping IP. Append latency to Collector object.
    =====================================================================
    """
    with open(ovpn) as s:
        x = s.readlines()[13] #<--What is this.
        ip = x.split(' ')[1]
        arg_pre_formating = 'ping -c 3 -w 3.5 ' + ip + ' | grep "mdev = "'
        arg = sysencode(arg_pre_formating)
        try:
            ping = getoutput(arg) #<-important.
            delay = ping.split()[3].split('/')[0] #<--What is this.
            Collector.souls.append({
                'name': ovpn.split('/')[-1], #<--What is this.
                'ip': ip,
                'latency': float(delay)
            })
        except IndexError as e:
            Collector.errors.append(e)

def show_top_10():
    """
    Step 3: show the top 10 results. Pretty self-explanatory.
    =========================================================
    """
    Collector.show()
    pass

def connect_vpn(pass_file_pth):
    """
    Step 4: Add credentials to file for fastest ovpn file. Connect to VPN.
    ======================================================================
    """

    print('Connecting to {}...'.format(Collector.chicken_dinner()))

    with open(Collector.chicken_dinner()) as ovpn_read:
        if not any(
            'auth-user-pass ' + pass_file_pth in line
            for line in ovpn_read.readlines()
        ):

            with open(Collector.chicken_dinner(), 'a+') as uName:
                print('writing credential reference')
                uName.write('auth-user-pass ' + pass_file_pth + '\n')
                uName.write('dhcp-option DNS 8.8.8.8')
            with open(Collector.chicken_dinner()) as uName:
                print(str([line for line in uName.readlines()][-2:]))

    with open('connect_vpn.sh', 'w') as c:
        c.write('sudo openvpn ' + Collector.chicken_dinner())

    start_vpn = str('sudo openvpn ' + Collector.chicken_dinner())
    call(start_vpn, shell=True)


def main(passfile='realpass.txt',refresh=False, connect=False):
    assert path.exists(path.realpath(passfile))
    #TODO add update servers check 24 hour
    #TODO: DO YOU WANT TO KEEP THIS SCRIPT RUNNING IN THE BACKGROUND ALWAYS OR DO YOU WANT TO MODIFY CRONTAB?
    if refresh:
        update_servers()

    threadPool()

    show_top_10()

    print(Collector.chicken_dinner())

    if connect:
        connect_vpn(passfile)

if __name__ == '__main__':
    main(refresh=False, connect=True)
