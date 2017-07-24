from __future__ import print_function
__doc__ = ''' All in one for updating vpn files, pinging vpn, connecting to vpn with credentials file'''

from speedyvpn import get_scripts
from speedyvpn.core.Collector import Collector
from speedyvpn.utils.compat import sysencode
from speedyvpn.core.update import update

from os import path
import os
from glob import glob
from multiprocessing.dummy import Pool
from subprocess import call, getoutput


def update_servers(*args):
    """
    Step 1: [OPTIONAL] update the list of VPN servers to check.
    ===========================================================
    """
    if not args:
        update()
    else:
        update(args[0])


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


def get_servers(ovpn_root_dir=os.environ['HOME'], retry=False):
    """
    Step 2a: match tcp servers in the US in ovpn folder.
    ====================================================
    """
    match = 'us'
    if Collector.ovpn_dir_path:
        ovpn_targets = glob(os.path.join(Collector.ovpn_dir_path, match + '*' + 'tcp*'))
        # print('if', ovpn_targets)
    else:
        ovpn_targets = glob(ovpn_root_dir + '/.speedyvpn/' + match + '*' + 'tcp*')
        # print('else', ovpn_targets)
    if len(ovpn_targets) < 1:
        if retry == False:
            update_servers()
            return get_servers(retry=True)
        else:
            raise Exception('No ovpn files saved')
    return ovpn_targets


def cycle(ovpn):
    """
    Step 2b: Read ovpn file, ping IP. Append latency to Collector object.
    =====================================================================
    """
    with open(ovpn) as s:
        x = s.readlines()[13]  #<--What is this. 
        ''' ANSWER: BADMAN TING!!! Nord's server IP is on line 13 of their ovpn files 
        This is a lazy hack and will break if anythin changes :0, needs to be regex. '''
        ip = x.split(' ')[1]

        arg = sysencode('ping -c 3 -w 3.5 ' + ip + ' | grep "mdev = "')

        try:
            ping = getoutput(arg)  #<-important.
            delay = ping.split()[3].split('/')[0]  #<--What is this.
            ''' ANSWER: Opaque str maniupulation for opaque bash call:
            $ ping -c 3 -w 3.5 8.8.8.8 | grep "mdev = "
            Meaning "ping this IP 3 times, timeout if  t > 3.5 seconds and grab the final line of output (that contains the average t). 

            Typical response: "rtt min/avg/max/mdev = 19.982/20.122/20.267/0.164 ms"

            THEN use this python string parsing to take the 'AVE' number, taking 2nd '/' split of 3rd ' ' split
            '''

            Collector.souls.append(
                {
                    'name': ovpn.split('/')[-1],  #<--What is this. 
                    'ip': ip,
                    'latency': float(delay)
                }
            )
            ''' ANSWER: me using split indexing instead of os.path.basename to get the filename. path.basename is better. '''
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
    try:
        chicken_for_all_meals = Collector.chicken_dinner()
        assert path.exists(chicken_for_all_meals)
    except AssertionError:
        chicken_for_all_meals = os.path.join(os.environ['HOME'], Collector.chicken_dinner())
    print('Connecting via {}...'.format(chicken_for_all_meals))

    with open(chicken_for_all_meals) as ovpn_read:
        if not any('auth-user-pass ' + pass_file_pth in line for line in ovpn_read.readlines()):

            with open(chicken_for_all_meals, 'ab+') as uName:
                print('writing credential reference')
                uName.write('auth-user-pass ' + pass_file_pth + '\n')
                uName.write('dhcp-option DNS 8.8.8.8')
            with open(chicken_for_all_meals) as uName:
                print(str([line for line in uName.readlines()][-2:]))

    # again, using get_scripts() to bring the shell scripts with the package when installing from pip.
    connect_vpn_shell_script = get_scripts('connect_vpn.sh')

    with open(connect_vpn_shell_script, 'wb+') as c:
        c.write(sysencode(str('sudo openvpn ' + chicken_for_all_meals)))

    start_vpn = sysencode(str('sudo openvpn ' + chicken_for_all_meals))

    # DUDE shell=True?! BAYD BAYD BAYD BAYD BAYD BAYD BAAAAYYAYAYAYAYAYAAYDDDDDD NOT GOOD BAYD.
    # that said, to fix this we'll need to instruct python to make a child process.
    #TODO: create a module which creates & "passes the baton" to a child-process.
    ''' ANSWER: cool, you'll need to explain this to me '''
    #TODO: wait... why shell=True is bad? POOR FORM. PERIOD. (aka Idk but smart ppl say: DONT)
    call(start_vpn, shell=True)


def main(passfile=None, refresh=True, connect=False):

    if passfile and not path.exists(path.realpath(passfile)):
        raise IOError(
            'the path to `passfile` does not exist. Check your syntax & ensure your file exists.'
        )

    #TODO add update servers check 24 hour
    #TODO: DO YOU WANT TO KEEP THIS SCRIPT RUNNING IN THE BACKGROUND ALWAYS OR DO YOU WANT TO MODIFY CRONTAB?
    ''' ANSWER How about a variable along the lines of  'refresh servers if it's been > X hours' 
        Would rather keep this program contained than fuck with system processes.
    '''
    #TODO: I agree. Windows & mac don't have cron.
    #TODO: What do you think about making a seperate daemon process that calls this one? yah?
    if refresh:
        update_servers()

    threadPool()

    show_top_10()

    print(Collector.chicken_dinner())

    # putting the password-check down here because it's the only part that needs the password.
    if passfile and not connect:
        raise AssertionError("you passed in a uname & password but didn't ask to connect to anything.")

    if connect:
        if not passfile:
            raise IOError('please pass in a text file in the format: username + newline + password.')
        connect_vpn(passfile)
    else: exit(0)

if __name__ == '__main__':
    main(refresh=False, connect=True)
