#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import xml.etree.ElementTree as ET
import sys

markerId = 1

CHANNEL_TSID = '270F'

reload(sys)
sys.setdefaultencoding('UTF-8')


def getURLProperty(node, property):
    prop = node.get(property)
    if prop is not None:
        result = urllib.quote_plus(prop)
    return result


def getChannelService(service, channel, long=True):
    channelId = service.attrib.get('id')
    serviceId = service.attrib.get('sid')
    serviceType = service.attrib.get('type')
    channelService = ''
    if serviceId is not None and channelId is None:
        channelService = serviceId
    if channel is not None:
        if serviceId is not None:
            channelService = serviceId
        else:
            if serviceType is None:
                channelService = '1:0:19'
            else:
                channelService = '1:0:'+format(int(serviceType), 'X')
            channelService += ':'+format(int(channelId), 'X')+':'+CHANNEL_TSID+':0:0:0:0:0:'
        channelService += getURLProperty(channel, 'url')+':'
    else:
        if serviceId is not None:
            channelService = serviceId
    return channelService


def getChannelName(service, channel):
    channelName = ''
    name = service.attrib.get('name')
    if name is not None:
        channelName = name
    else:
        if channel is not None:
            channelName = channel.text
    return channelName


def findChannel(channels, channelId):
    channel = None
    if channelId is not None:
        channel = channels.find('Channel[@id="'+channelId+'"]')
    return channel


def writeService(bouquetFile, service, name):
    if service != '':
        bouquetFile.write(('#SERVICE '+service+name+'\n').encode('UTF-8'))
        if name != '':
            bouquetFile.write(('#DESCRIPTION '+name+'\n').encode('UTF-8'))


def writeMarker(bouquetFile, name):
    global markerId
    service = '1:64:'+str(markerId)+':0:0:0:0:0:0:0::'
    writeService(bouquetFile, service, name)
    markerId += 1


def writeGroup(bouquetFile, name, channels):
    group = channels.findall('Channel[@group="'+name+'"]')
    for entry in group:
        channelId = entry.attrib.get('id')
        channel = findChannel(channels, channelId)
        channelService = getChannelService(entry, channel)
        channelName = getChannelName(entry, channel)
        writeService(bouquetFile, channelService, channelName)


def writeChannel(bouquetFile, channelId, service, channels):
    channel = None
    if channelId is not None:
        channel = channels.find('Channel[@id="'+channelId+'"]')
    channelService = getChannelService(service, channel)
    channelName = getChannelName(service, channel)
    writeService(bouquetFile, channelService, channelName)


def writeEnigmaUserBouquet(bouquetFile, bouquet, channels):
    for element in bouquet.iter():
        name = element.attrib.get('name')
        channelId = element.attrib.get('id')
        if element.tag == 'Bouquet' and name is not None:
            bouquetFile.write('#NAME '+name+'\n')
        elif element.tag == 'Marker' and name is not None:
            writeMarker(bouquetFile, name)
        elif element.tag == 'Group' and name is not None:
            writeGroup(bouquetFile, name, channels)
        elif element.tag == 'Service':
            writeChannel(bouquetFile, channelId, element, channels)


def main():
    if len(sys.argv) != 2:
        print 'usage: '+sys.argv[0]+' <bouquetXMLfile>'
        sys.exit(2)
    bouquet = ET.parse(sys.argv[1]).getroot()
    channelsFile = bouquet.attrib.get('channels')
    bouquetFile = bouquet.attrib.get('file')
    channels = ET.parse(channelsFile)
    with open(bouquetFile, 'w') as bouquetFile:
        writeEnigmaUserBouquet(bouquetFile, bouquet, channels)
    # writeEPGImportChannels(bouquet, channels)


if __name__ == '__main__':
    main()
