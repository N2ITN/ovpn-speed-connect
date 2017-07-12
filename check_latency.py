from glob import glob
from subprocess import check_output
from multiprocessing.dummy import Pool


class HighSchoolGuidanceCounselor(object):
    """ Collect thread worker results, provide formatting """
    
    def __new__(cls, *args, **kwargs):
        cls.souls = []
        cls.errors = []

    def __init__(self):
        super(HighSchoolGuidanceCounselor, self).__init__()

    @classmethod
    def show(cls):
        """ 
        Sort list of dictionaries by dictionary attribute 'latency' 
        Pretty print top 10 results by server name and latency
        """

        listicle = sorted(
            cls.souls, key=lambda x: float(x['latency'])
        )
        all_ = [[x['latency'], x['name'].split('.')[0]]
                for x in listicle][:10]
        print('Server \t Latency')
        for pair in [all_[x] for x in range(10)]:
            print('{} \t {}'.format(pair[1], pair[0]))

    @classmethod
    def cycle(cls, ovpn):
        """ 
        Read opvn file, ping IP in bash one time with 1 second timeout
        Parse result, append latency to HighSchoolGuidanceCounselor object.
        """
        with open(ovpn) as s:
            x = s.readlines()[13]
            ip = x.split(' ')[1]
            arg = 'ping -c 1 -w 1 ' + ip
            try:
                ping = check_output(arg.split(' '))
                delay = str(ping).split('time=')[1].split(' ')[0]
                cls.souls.append({
                    'name': ovpn.split('/')[-1],
                    'ip': ip,
                    'latency': delay
                })
            except Exception as e:
                cls.errors.append(e)


def threadPool(all_opvn):
    """ DO IT 100 TIMES AT ONCE """
    for i in Pool(100).imap(HighSchoolGuidanceCounselor.cycle, all_opvn):
        pass

def main():
    # Soooo when I'm gonna use a singleton class, I usually use it as a runtime memory-cache.
    # That said, singletons in a script this short are usually for conceptualization.

    # THEREFORE: I feel like soma' my changes may be subjective :/

    # Not this main() function tho. GLOBALS R BAD.
    # Now you can import this module without running it! ^_^

    init_the_guidance = HighSchoolGuidanceCounselor()
    # superfluous but fuckit.
    assert 'souls', 'errors' in vars(init_the_guidance).keys()

    """ match tcp servers in the US in ovpn folder"""
    match = 'us'
    
    all_opvn = glob('./OVPN/' + match + '*' + 'tcp*')
    
    threadPool(all_opvn=all_opvn)
    
    """ Show top 10 results """
    HighSchoolGuidanceCounselor.show()

if __name__ == '__main__':
    main()