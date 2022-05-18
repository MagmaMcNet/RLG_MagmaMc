#!/usr/bin/python

# Utility to forward ports on your router using UPnP
# most code from  http://mattscodecave.com/posts/using-python-and-upnp-to-forward-a-port
# - adapted for command line use
# - support multiple routers in the lan

import socket
import re
from urlparse import urlparse
import urllib2
from xml.dom.minidom import parseString
from xml.dom.minidom import Document
import httplib
import time
import argparse
import sys

def discover():
    """Discover UPNP capable routers in the local network
    Returns a lit of urls with service descriptions
    """
    SSDP_ADDR = "239.255.255.250"
    SSDP_PORT = 1900
    SSDP_MX = 2
    SSDP_ST = "urn:schemas-upnp-org:device:InternetGatewayDevice:1"

    WAIT = 1

    ssdpRequest = "M-SEARCH * HTTP/1.1\r\n" + \
                    "HOST: %s:%d\r\n" % (SSDP_ADDR, SSDP_PORT) + \
                    "MAN: \"ssdp:discover\"\r\n" + \
                    "MX: %d\r\n" % (SSDP_MX, ) + \
                    "ST: %s\r\n" % (SSDP_ST, ) + "\r\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)
    sock.sendto(ssdpRequest, (SSDP_ADDR, SSDP_PORT))
    time.sleep(WAIT)
    paths = []
    for _ in range(10):
        try:
            data, fromaddr = sock.recvfrom(1024)
            ip = fromaddr[0]
            #print "from ip: %s"%ip
            parsed = re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', data)

            # get the location header
            location = filter(lambda x: x[0].lower() == "location", parsed)

            # use the urlparse function to create an easy to use object to hold a URL
            router_path = location[0][1]
            paths.append(router_path)

        except socket.error:
            '''no data yet'''
            break
    return paths


def get_wanip_path(upnp_url):
    # get the profile xml file and read it into a variable
    directory = urllib2.urlopen(upnp_url).read()

    # create a DOM object that represents the `directory` document
    dom = parseString(directory)

    # find all 'serviceType' elements
    service_types = dom.getElementsByTagName('serviceType')

    # iterate over service_types until we get either WANIPConnection
    # (this should also check for WANPPPConnection, which, if I remember correctly
    # exposed a similar SOAP interface on ADSL routers.
    for service in service_types:
        # I'm using the fact that a 'serviceType' element contains a single text node, who's data can
        # be accessed by the 'data' attribute.
        # When I find the right element, I take a step up into its parent and search for 'controlURL'
        if service.childNodes[0].data.find('WANIPConnection') > 0:
            path = service.parentNode.getElementsByTagName('controlURL')[0].childNodes[0].data
            return path

def open_port(service_url,external_port,internal_client,internal_port=None,protocol='TCP',duration=0,description=None,enabled=1):
    parsedurl = urlparse(service_url)

    if internal_port==None:
        internal_port = external_port

    if description == None:
        description = 'FILEZ'

    if not enabled:
        duration=1

    doc = Document()

    # create the envelope element and set its attributes
    envelope = doc.createElementNS('', 's:Envelope')
    envelope.setAttribute('xmlns:s', 'http://schemas.xmlsoap.org/soap/envelope/')
    envelope.setAttribute('s:encodingStyle', 'http://schemas.xmlsoap.org/soap/encoding/')

    # create the body element
    body = doc.createElementNS('', 's:Body')

    # create the function element and set its attribute
    fn = doc.createElementNS('', 'u:AddPortMapping')
    fn.setAttribute('xmlns:u', 'urn:schemas-upnp-org:service:WANIPConnection:1')

    # setup the argument element names and values
    # using a list of tuples to preserve order
    arguments = [
        ('NewRemoteHost', ""), # unused - but required
        ('NewExternalPort', external_port),           # specify port on router
        ('NewProtocol', protocol),                 # specify protocol
        ('NewInternalPort', internal_port),           # specify port on internal host
        ('NewInternalClient', internal_client), # specify IP of internal host
        ('NewEnabled', enabled),                    # turn mapping ON
        ('NewPortMappingDescription', description), # add a description
        ('NewLeaseDuration', duration)]              # how long should it be opened?

    # NewEnabled should be 1 by default, but better supply it.
    # NewPortMappingDescription Can be anything you want, even an empty string.
    # NewLeaseDuration can be any integer BUT some UPnP devices don't support it,
    # so set it to 0 for better compatibility.

    # container for created nodes
    argument_list = []

    # iterate over arguments, create nodes, create text nodes,
    # append text nodes to nodes, and finally add the ready product
    # to argument_list
    for k, v in arguments:
        v = str(v)
        tmp_node = doc.createElement(k)
        tmp_text_node = doc.createTextNode(v)
        tmp_node.appendChild(tmp_text_node)
        argument_list.append(tmp_node)

    # append the prepared argument nodes to the function element
    for arg in argument_list:
        fn.appendChild(arg)

    # append function element to the body element
    body.appendChild(fn)

    # append body element to envelope element
    envelope.appendChild(body)

    # append envelope element to document, making it the root element
    doc.appendChild(envelope)

    # our tree is ready, conver it to a string
    pure_xml = doc.toxml()

    # use the object returned by urlparse.urlparse to get the hostname and port
    conn = httplib.HTTPConnection(parsedurl.hostname, parsedurl.port)

    # use the path of WANIPConnection (or WANPPPConnection) to target that service,
    # insert the xml payload,
    # add two headers to make tell the server what we're sending exactly.
    conn.request('POST',
        parsedurl.path,
        pure_xml,
        {'SOAPAction': '"urn:schemas-upnp-org:service:WANIPConnection:1#AddPortMapping"',
         'Content-Type': 'text/xml'}
    )

    # wait for a response
    resp = conn.getresponse()

    return resp.status,resp.read()


def get_my_ip(routerip=None):
    if routerip==None:
        routerip="8.8.8.8" #default route
    ret = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((routerip,80))
        ret = s.getsockname()[0]
        s.close()
    except:
        pass
    return ret


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="verbose output",
                    action="store_true")
    parser.add_argument("-e", "--external-port", type=int,
                    help="external port to open",dest="eport")
    parser.add_argument("-l", "--local-port", type=int,
                    help="internal port (default: same as external)",dest="iport", default=None)
    parser.add_argument("-i", "--lan-ip",
                help="lan-ip where to forward the port, this computer if not specified",dest="lanip", default=None)
    parser.add_argument("-r", "--router",
                    help="router ip to use. by default uses all discovered routers",action='append')
    parser.add_argument("-p","--protocol",default='TCP', help="TCP or UDP")
    parser.add_argument("-d", "--description",help="description for the rule")
    parser.add_argument("--disable", action='store_true',dest='disable', help="disable a existing forwarding")
    parser.add_argument("-t","--time", type=int, help="Duration of the rule",default=0)
    args = parser.parse_args()
    args.eport = 8081
    if args.verbose:
        print "Discovering routers..."

    res = discover()
    if args.verbose or args.eport==None:
        print "Found %s UPnP routers: "%len(res)," ".join([urlparse(x).netloc for x in res])

    if args.eport==None:
        print "No external port specified."
        sys.exit(0)

    if args.iport == None:
        args.iport = args.eport

    allok = True
    for path in res:
        discparsed = urlparse(path)
        service_path = get_wanip_path(path)
        service_url = "%s://%s%s"%(discparsed.scheme,discparsed.netloc,service_path)
        routerip = discparsed.netloc.split(':')[0]
        if args.router!=None and routerip not in args.router:
            continue

        localip = args.lanip
        if args.lanip == None:
            localip = get_my_ip(routerip)

        enabled = int(not args.disable)

        dis=''
        if not enabled:
            dis='disable of '

        status,message = open_port(path,args.eport,internal_client=localip,internal_port=args.iport,protocol=args.protocol,duration=args.time,description=args.description,enabled = enabled)
        if status==200:

            if args.verbose:
                print "%sport forward on %s successful, %s->%s:%s"%(dis,routerip,args.eport,localip,args.iport)
        else:
            sys.stderr.write("%sport forward on %s failed, status=%s message=%s\n"%(dis,routerip,status,message))
            allok = False


    if allok:
        sys.exit(0)
    else:
        sys.exit(1)
