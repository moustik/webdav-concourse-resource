#!/usr/bin/env python3

import sys
import os.path

from datetime import datetime
import json

import webdav3.client as wc


def get_timestamp(client, p):
    date_string = client.info(p)['modified']
    datetime_object = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
    return int(datetime_object.timestamp())


def _check(json_in):
    watched_folder = json_in.get("source").get("watch_folder")
    options = json_in.get("source")

    client = wc.Client(options)

    previous_version = json_in.get("version")
    if previous_version:
        previous_version = int(previous_version.get("version"))
    else:
        previous_version = 0
    version = None
    if client.check(watched_folder):
        version = get_timestamp(client, watched_folder)

    json_data = []
    if version > previous_version:
        json_data.append({
            'version': str(version),
            'from': str(previous_version)
            })

    print(json.dumps(json_data))


def _in(json_in):
    dest_dir = sys.argv[1]
    timestamp = json_in.get("version", {}).get("from")
    watched_folder = json_in.get("source").get("watch_folder")

    options = json_in.get("source")
    client = wc.Client(options)
    picture_list = client.list(watched_folder)[1:]
    new_pix = list(filter(lambda p: get_timestamp(client, os.path.join(watched_folder, p)) > int(timestamp), picture_list))

    with open(os.path.join(dest_dir, "pix.json"), "w") as outfile:
        json.dump(new_pix, outfile)

    print(json.dumps(json_in))


callbacks = {
    "in": _in,
    "check": _check,
    }


if __name__ == "__main__":
    input_data = "".join(sys.stdin.readlines())
    data = json.loads(input_data)

    with open("/input", "w") as f:
        f.write(input_data)
    callbacks.get(os.path.basename(sys.argv[0]))(data)
