#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import urllib.request, urllib.parse, urllib.error
import xmltodict
import datetime

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

config = dict()

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()


def get_overview(hermes, intent_message):
    result_sentence = ""

    file = urllib.request.urlopen(config["service"]["feed_url"])
    data = file.read()
    file.close()
    dict = xmltodict.parse(data)

    titles = ""
    for item in data['rss']['channel']['item']:
        titles = titles + "\n" + item['title']

    if len(titles) > 0:
        result_sentence = "Ich habe folgende Nachrichten gefunden:" + titles
    else:
        result_sentence = "Es gibt nichts Neues."

    hermes.publish_end_session(intent_message.session_id, result_sentence)


if __name__ == "__main__":
    config = read_configuration_file(CONFIG_INI)

    if config.get("service").get("feed_url") is None:
        print "No feed URL key in config.ini, you must setup an RSS feed URL for this skill to work"
        sys.exit(1)

    with Hermes(MQTT_ADDR.encode("ascii")) as h:
        h.subscribe_intent("GetRssReaderOverview",
                           get_overview) \
        .loop_forever()
