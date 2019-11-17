# Snips RSS reader action
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/JBosecker/snips-skill-rss-reader/master/LICENSE)

This is a Snips RSS reader action written in Python and is compatible with `snips-skill-server`.
It will pull the data from the configured RSS feed and read the titles as an overview.

## Skill Setup
### Prerequisites

You'll need to add the RSS reader skill in your assistant. It's available on [Snips' console](https://console.snips.ai)

### SAM (preferred)
Just install your assistant through SAM and the action will also be installed automatically.

### Manually

Copy it manually to the device to the folder `/var/lib/snips/skills/`
You'll need `snips-skill-server` installed on the pi

`sudo apt-get install snips-skill-server`

Stop snips-skill-server & generate the virtual environment
```
sudo systemctl stop snips-skill-server
cd /var/lib/snips/skills/snips-skill-rss-reader/
sh setup.sh
sudo systemctl start snips-skill-server
```

## How to trigger

`Hey Snips`

`Was gibt es Neues?`

## Logs
Show snips-skill-server logs with sam:

`sam service log snips-skill-server`

Or on the device:

`journalctl -f -u snips-skill-server`

Check general platform logs:

`sam watch`

Or on the device:

`snips-watch`
