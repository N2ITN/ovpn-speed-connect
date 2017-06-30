from glob import glob
from subprocess import check_output

from multiprocessing.dummy import Pool


class Collector:
    """ Collect thread worker results, provide formatting """
    souls = []
    errors = []

    def show():
        """ 
        Sort list of dictionaries by dictionary attribute 'latency' 
        Pretty print top 10 results by server name and latency
        """

        listicle = sorted(
            Collector.souls, key=lambda x: float(x['latency'])
        )
        all_ = [[x['latency'], x['name'].split('.')[0]]
                for x in listicle][:10]
        print('Server \t Latency')
        for pair in [all_[x] for x in range(10)]:
            print('{} \t {}'.format(pair[1], pair[0]))


""" match tcp servers in the US in ovpn folder"""
match = 'us'
all_opvn = glob('./OVPN/' + match + '*' + 'tcp*')


def cycle(ovpn):
    """ 
    Read opvn file, ping IP in bash one time with 1 second timeout
    Parse result, append latency to Collector object.
    """
    with open(ovpn) as s:
        x = s.readlines()[13]
        ip = x.split(' ')[1]
        arg = 'ping -c 1 -w 1 ' + ip
        try:
            ping = check_output(arg.split(' '))
            delay = str(ping).split('time=')[1].split(' ')[0]
            Collector.souls.append({
                'name': ovpn.split('/')[-1],
                'ip': ip,
                'latency': delay
            })
        except Exception as e:
            Collector.errors.append(e)


def threadPool():
    """ DO IT 100 TIMES AT ONCE """
    for i in Pool(100).imap(cycle, all_opvn):
        pass


threadPool()
""" Show top 10 results """
Collector.show()