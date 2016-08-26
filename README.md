# slackerr

[![Build Status](https://travis-ci.org/olanmatt/slackerr.svg)](https://travis-ci.org/olanmatt/slackerr)

Pipe directly to Slack from your shell

![demo](http://i.imgur.com/HBFTRcA.gif)

## Setup

Install with pip:
```sh
pip install --upgrade git+https://github.com/olanmatt/slackerr.git
```

You must generate a [Slack OAuth token](https://api.slack.com/docs/oauth-test-tokens). This token can be passed as an argument (see below).

Alternatively, any of the `CONFIG` or command line arguments can be persisted in `~/.slackerr` in JSON format.

For example:

```json
{
  "token": "xoxp-XXXXXXXXXXX-XXXXXXXXXXX-XXXXXXXXXXX-XXXXXXXXXX",
  "channel": "random",
  "username": "mybot",
  "verbose": true
}
```

## Usage

```sh
slackerr [options] [message]
```

### Options
```
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Slack API authentication token
  -c CHANNEL, --channel CHANNEL
                        specify the channel to send to
  -u USERNAME, --username USERNAME
                        specify the username to send as
  --formatted           assume message is preformatted
  --live                actively send from stdin
  -v, --verbose         increase output verbosity
```

### Examples

```sh
ls -l | slackerr
```

```sh
slackerr < README.md
```

```sh
tail -f some.log | ./slackerr --live
```

```sh
slackerr --username olanmatt --channel bots "Hello, world!"
```

```sh
slackerr --formatted "*Hello*, _world_!"
```
