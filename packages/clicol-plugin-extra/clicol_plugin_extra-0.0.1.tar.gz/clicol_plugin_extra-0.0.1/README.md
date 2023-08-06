CLICOL PLUGIN EXTRAS
====================
Plugins for [clicol](https://github.com/realvitya/clicol) which help troubleshooting by integrating handy tools.

## Example

### macvendor

inline output:

     1    000a.b82d.10e0(Cisco Systems, Inc)    DYNAMIC     Fa0/16
     1    0012.80b6.4cd8(Cisco Systems, Inc)    DYNAMIC     Fa0/3
     1    0012.80b6.4cd9(Cisco Systems, Inc)    DYNAMIC     Fa0/16

append output:

    320 9cf4.8ee4.f398  dynamic  Yes      300     Po1                             MAC: Apple, Inc.
    101 f8ca.b819.2dfc  dynamic  Yes        0     Po2                             MAC: Dell Inc.

### ipcalc
    After breaking and command 'I':
    IP: 192.168.0.2 255.255.255.224
    ipaddress:	192.168.0.2
    network/nm:	192.168.0.0/27
    prefixlen:	27
    netmask:	255.255.255.224
    wildcard:	0.0.0.31
    network:	192.168.0.0
    broadcast:	192.168.0.31
    number of ips:	32 - 2 = 30
    first host:	192.168.0.1
    last host:	192.168.0.30

### dnsresolve
    After breaking and command 'R':
    IP/NAME: 8.8.8.8
    Host: dns.google, aliases: [], ipaddrlist: ['8.8.8.8']
    IP/NAME: github.com
    Host: lb-140-82-118-4-ams.github.com, aliases: [], ipaddrlist: ['140.82.118.4']

## Configuration

In `~/.clicol/plugins.cfg` there must be a section for the plugin.

Example with defaults:

     # MAC vendor lookup
     [macvendor]
     # set 'no' to disable
     #active=yes
     # view (append|inline)
     #outtype=inline
     
     [ipcalc]
     # set 'no' to disable
     #active=yes

     [dnsresolve]
     # set 'no' to disable
     #active=yes
