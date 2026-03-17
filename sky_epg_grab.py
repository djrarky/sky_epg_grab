#!/usr/bin/python3

import os
import sys
import requests
import json
import time
import datetime
import xml.etree.cElementTree as ET
from itertools import islice

def get_channel_details(channel_details_uri):
    sky_channel_details = json.loads(requests.get(channel_details_uri).content)
    channels = {}
    for channel in sky_channel_details['services']:
        channel_number = channel.get("c", "")
        channel_title = channel.get("t", "")
        sid = channel.get("sid", "")
        channels[channel_number] = [channel_title, sid]
    return channels

def open_xml():
    return ET.Element("tv")

def write_xml(root, filename):
    tree = ET.ElementTree(root)
    tree.write(filename)

def write_channel_xml(root, channel_details):
    for channel_number, (channel_name, sid) in channel_details.items():
        channel_xml = ET.SubElement(root, 'channel')
        channel_xml.set('id', f"{channel_number}.uk")
        ET.SubElement(channel_xml, "display-name").text = channel_name
        ET.SubElement(channel_xml, "display-name").text = channel_number
        icon_uri = f"https://d2n0069hmnqmmx.cloudfront.net/epgdata/1.0/newchanlogos/10000/10000/skychb{sid}.png"
        ET.SubElement(channel_xml, "icon").set('src', icon_uri)
    return root

def get_listings(uri):
    return json.loads(requests.get(uri).content)

def get_program_image_url(program_id, aspect_ratio="16-9", size="1200"):
    return f"https://images.metadata.sky.com/pd-image/{program_id}/{aspect_ratio}/{size}"

def programs(days_listings, root, sid_to_channel):
    for schedule in days_listings['schedule']:
        channel_id = sid_to_channel.get(schedule['sid'], schedule['sid'])
        for program in schedule['events']:
            start_time = time.strftime('%Y%m%d%H%M%S', time.gmtime(program['st']))
            end_time = time.strftime('%Y%m%d%H%M%S', time.gmtime(program['st'] + program['d']))

            program_xml = ET.SubElement(root, 'programme')
            program_xml.set('start', start_time)
            program_xml.set('stop', end_time)
            program_xml.set('channel', channel_id)

            ET.SubElement(program_xml, "title").text = program.get('t', '')
            if 'sy' in program:
                ET.SubElement(program_xml, "desc").text = program['sy']
            if 'programmeuuid' in program:
                image_url = get_program_image_url(program['programmeuuid'])
                ET.SubElement(program_xml, "icon").set('src', image_url)
    return root

def chunks(data, size=10):
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k: data[k] for k in islice(it, size)}

def get_epg_uris(channel_details, root, days):
    sid_to_channel = {sid: f"{num}.uk" for num, (_, sid) in channel_details.items()}
    for sid_chunk in chunks(channel_details, 10):
        sids = [v[1] for v in sid_chunk.values() if v[1]]
        sid_string = ','.join(sids)
        for day_offset in range(days):
            date = (datetime.datetime.now() + datetime.timedelta(days=day_offset)).strftime('%Y%m%d')
            epg_url = f"https://awk.epgsky.com/hawk/linear/schedule/{date}/{sid_string}"
            day_listings = get_listings(epg_url)
            root = programs(day_listings, root, sid_to_channel)

def get_sky_epg_data(filename, days, region):
    channel_details_uri = f"https://awk.epgsky.com/hawk/linear/services/4101/{region}"
    channel_details = get_channel_details(channel_details_uri)
    root = open_xml()
    root = write_channel_xml(root, channel_details)
    get_epg_uris(channel_details, root, days)
    write_xml(root, filename)

if __name__ == "__main__":
    # Get values from environment variables or fall back to defaults
    region = int(os.getenv("REGION", 1))
    days = int(os.getenv("EPG_DAYS", 7))
    filename = sys.argv[1] if len(sys.argv) > 1 else "sky.xml"

    if days > 7 or days < 1:
        print("EPG_DAYS must be between 1 and 7")
        sys.exit(1)

    get_sky_epg_data(filename, days, region)
