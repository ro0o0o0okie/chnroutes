"""
Directely add/remove routes to the table for linux.
"""
import os, json
from chnroutes import fetch_ip_data
from multiprocessing import Pool, cpu_count
from route_win import LoadIpFromJson
#==============================================================================

def AddRouteMP(dataLst, gateway='192.168.11.1', metric=5, pool=None):
    Map = map if pool is None else pool.map
    addCmdLst = [ 'route add -net %s netmask %s gw %s metric %d'%(ip, mask, gateway, metric) 
                    for (ip, mask, mask2) in dataLst ]

    Map(os.system, addCmdLst)


def DelRouteMP(dataLst, pool=None):
    Map = map if pool is None else pool.map

    delCmdLst = [ 'route del -net %s netmask %s'%(ip,mask) for (ip, mask, mask2) in dataLst ]

    Map(os.system, delCmdLst)


#==============================================================================
if __name__ == '__main__':
    GATEWAY = '192.168.11.1'
    dataLst = fetch_ip_data(r'./delegated-apnic-latest.txt')
    # dataLst = LoadIpFromJson(r'./routes_cn.json')
    print('IP record number: %i'%len(dataLst))

    p = Pool(processes=4, maxtasksperchild=1000)
    #p = None
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

    p.close()
    p.join()
