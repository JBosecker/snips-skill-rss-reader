#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import urllib.request, urllib.parse, urllib.error
import xmltodict
import datetime

CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class Template(object):

    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        if self.config.get("global").get("feed_url") is None:
            print("No feed URL key in config.ini, you must setup an RSS feed URL for this skill to work")
            sys.exit(1)

        self.start_blocking()

    def get_overview(self, hermes, intent_message):
        result_sentence = ""

        file = urllib.request.urlopen(self.config["global"]["feed_url"])
        data = file.read()
        file.close()
        dict = xmltodict.parse(data)

        maximum_number_of_items = self.config["global"]["maximum_number_of_items"]
        if maximum_number_of_items is None:
            maximum_number_of_items = 5
        else
            maximum_number_of_items = int(maximum_number_of_items)

        titles = ""
        number = 0

        for item in dict['rss']['channel']['item']:
            number = number + 1
            titles = titles + "\n" + str(number) + ") " + item['title'] + "."

            if number >= maximum_number_of_items:
                break

        if number > 0:
            result_sentence = "Ich habe folgende Nachrichten gefunden:" + titles
        else:
            result_sentence = "Es gibt nichts Neues."

        hermes.publish_end_session(intent_message.session_id, result_sentence)

    def master_intent_callback(self, hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'Johannes:GetRssReaderOverview':
            self.get_overview(hermes, intent_message)

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    Template()
