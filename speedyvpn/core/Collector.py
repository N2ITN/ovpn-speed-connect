class Collector(object):
    """
    This is a singleton state-machine class which:
      - Collects thread worker results & stores them in-memory at runtime.
      - provides formatting

     """
    souls = []
    errors = []

    # using pass in the __new__ method prevents the creation of class-instances.
    # in other words, it forces this class to be a singleton.
    def __new__(cls, *args, **kwargs):
        pass

    # this is technically unnecessary.
    # __init__ is used to set initialization params of instances.
    # however due to the __new__ overwrite above, creating instances is not currently possible.
    def __init__(self, *args, **kwargs):
        super(Collector, self).__init__()

    # making these @classmethods gives them consistent access to class-state.
    # it also prevents you from having to call `Collector` by name from within itself...which is generally bad.
    @classmethod
    def sort_results(cls):
        listicle = sorted(cls.souls, key=lambda x: x['latency'])
        return listicle

    @classmethod
    def show(cls):
        """
        Sort list of dictionaries by dictionary attribute 'latency'
        Pretty print top 10 results by server name and latency
        """

        all_ = [[x['latency'], x['name'].split('.')[0]]
                for x in cls.sort_results()][:10]
        print('Server \t Latency')
        for pair in [all_[x] for x in range(10)]:
            print('{} \t {}'.format(pair[1], pair[0]))

    @classmethod
    def chicken_dinner(cls):
        return '/'.join(['OVPN', cls.sort_results()[0]['name']])