import argparse
import sys
from speedyvpn.utils.compat import sysencode

# Apperently an "entry point" main()-function needs to take arguments, but you aren't allowed to passed any to it.
# IDK. I'm told there are reasons.
def main(args=None):
    if not args:
        parser = argparse.ArgumentParser()
        #TODO: ADD ACTUAL ARGUMENTS.
        parser.add_argument('-a', '--all', action='store_true', default=True, help="run all functions & connect")
        parser.add_argument('-p', '--passfile', nargs="?", default=None, help="pass in a txt file containing your credentials to connect with.")

        # activates the `...action='store_true...'` logic.
        arrgs = parser.parse_args()

        # the only time rediculous if-else trees are acceptable:
        if arrgs.all:
            from speedyvpn.core import check_latency
            if arrgs.passfile:
                check_latency.main(arrgs.passfile, connect=True)
            else:
                check_latency.main()
    else:
        sys.stdout(sysencode('Good job you broke it.'))
        sys.exit(-1)

if __name__ == '__main__':
    main()