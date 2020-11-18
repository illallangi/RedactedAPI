# RedactedAPI
[![Docker Pulls](https://img.shields.io/docker/pulls/illallangi/redactedapi.svg)](https://hub.docker.com/r/illallangi/redactedapi)
[![Image Size](https://images.microbadger.com/badges/image/illallangi/redactedapi.svg)](https://microbadger.com/images/illallangi/redactedapi)
![Build](https://github.com/illallangi/RedactedAPI/workflows/Build/badge.svg)

Tool and Python bindings for the [Redacted](https://redacted.ch/) [API](https://redacted.ch/wiki.php?action=article&id=455)

## Installation

```shell
pip install git+git://github.com/illallangi/RedactedAPI.git
```

## Usage

```shell
$ redacted-tool
Usage: redacted-tool [OPTIONS] COMMAND [ARGS]...

Options:
  --log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG|SUCCESS|TRACE]
  --slack-webhook TEXT
  --slack-username TEXT
  --slack-format TEXT
  --help                          Show this message and exit.

Commands:
  get-directory
  get-group
  get-index
  get-torrent
  rename-torrent-file
```
