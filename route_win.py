"""
Directely add/remove routes to the table for windows without BAT.
"""
import os
from chnroutes import fetch_ip_data
from multiprocessing import Pool, cpu_count
#==============================================================================

def AddRouteMP(dataLst, gateway='192.168.11.1', metric=5, pool=None):
    Map = map if pool is None else pool.map
    addCmdLst = [ 'route ADD %s MASK %s %s METRIC %d'%(ip, mask, gateway, metric) 
                    for (ip, mask, mask2) in dataLst ]

    os.system('ipconfig /flushdns') # clear dns 1st
    Map(os.system, addCmdLst)


def DelRouteMP(dataLst, pool=None):
    Map = map if pool is None else pool.map

    delCmdLst = [ 'route DELETE %s'%ip for (ip, mask, mask2) in dataLst ]

    Map(os.system, delCmdLst)

#==============================================================================
if __name__ == '__main__':
    GATEWAY = '192.168.11.1'
    localFn = r'./delegated-apnic-latest.txt' # use None to fetch latest
    
    dataLst = fetch_ip_data(localFn)
    print('IP record number: %i'%len(dataLst))

    p = Pool(processes=cpu_count(), maxtasksperchild=1000)
    # p = None
    done = False
    while not done:
        arg=raw_input('[A]dd or [D]elele routes (or [E]xit):\n-->>')
        if arg=='A' or arg=='a':
            AddRouteMP(dataLst, gateway=GATEWAY, metric=5, pool=p)
            done = True
        elif arg=='D' or arg=='d':
            DelRouteMP(dataLst, pool=p)
            done = True
        elif arg=='E' or arg=='e':
            done = True
        else:
            print('InputError.\n')

    p.close(); p.join()