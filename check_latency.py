''' All in one for updating vpn files, pinging vpn, connecting to vpn with credentials file'''
from glob import glob
from multiprocessing.dummy import Pool
from subprocess import call, check_output, getoutput
import subprocess

passFile = 'realpass.txt'


class Collector:
    """ Collect thread worker results, provide formatting """
    souls = []
    errors = []

    def sort_results():
        listicle = sorted(Collector.souls, key=lambda x: x['latency'])
        return listicle

    def show():
        """ 
        Sort list of dictionaries by dictionary attribute 'latency' 
        Pretty print top 10 results by server name and latency
        """

        all_ = [[x['latency'], x['name'].split('.')[0]]
                for x in Collector.sort_results()][:10]
        print('Server \t Latency')
        for pair in [all_[x] for x in range(10)]:
            print('{} \t {}'.format(pair[1], pair[0]))

    def chicken_dinner():

        return '/'.join(['OVPN', Collector.sort_results()[0]['name']])


def cycle(ovpn):
    """ 
    Read opvn file, ping IP in bash one time with 1 second timeout
    Parse result, append latency to Collector object.
    """

    with open(ovpn) as s:
        x = s.readlines()[13]
        ip = x.split(' ')[1]
        arg = 'ping -c 3 -w 3.5 ' + ip + ' | grep "mdev = "'
        try:
            ping = getoutput(arg)
            delay = ping.split()[3].split('/')[0]
            Collector.souls.append({
                'name': ovpn.split('/')[-1],
                'ip': ip,
                'latency': float(delay)
            })
        except IndexError as e:

            Collector.errors.append(e)


def threadPool():
    """ DO IT 100 TIMES AT ONCE """
    for i in Pool(300).imap(cycle, get_servers()):
        pass


def get_servers():
    """ match tcp servers in the US in ovpn folder"""
    match = 'us'
    opvn_targets = glob('./OVPN/' + match + '*' + 'tcp*')
    assert len(opvn_targets) > 1
    return opvn_targets


def update_servers():
    """ Updates the servers """
    call(['sudo', 'bash', 'update_servers.sh'])


def connect_vpn():
    """ Add credentials to file for fastest ovpn file """

    print('Connecting to {}...'.format(Collector.chicken_dinner()))

    with open(Collector.chicken_dinner()) as ovpn_read:
        if not any(
            'auth-user-pass ' + passFile in line
            for line in ovpn_read.readlines()
        ):

            with open(Collector.chicken_dinner(), 'a+') as uName:
                print('writing credential reference')
                uName.write('auth-user-pass ' + passFile + '\n')
                uName.write('dhcp-option DNS 8.8.8.8')
            with open(Collector.chicken_dinner()) as uName:
                print(str([line for line in uName.readlines()][-2:]))

    with open('connect_vpn.sh', 'w') as c:
        c.write('sudo openvpn ' + Collector.chicken_dinner())

    start_vpn = str('sudo openvpn ' + Collector.chicken_dinner())
    call(start_vpn, shell=True)


def top_10():
    Collector.show()


def main(refresh=False, connect=False):
    #TODO add update servers check 24 hour 
    if refresh:
        update_servers()

    threadPool()
    Collector.show()

    print(Collector.chicken_dinner())
    if connect:
        connect_vpn()


main(refresh=False, connect=True)
