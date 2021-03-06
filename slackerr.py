#!/usr/bin/env python

import argparse
import json
import os
import pprint
import sys
from slackclient import SlackClient

# Configuration defaults
CONFIG = {
    "channel": "general",
    "emoji": ":robot_face:",
    "username": "slackerr",
    "verbose": False,
}


def vprint(*args):
    if CONFIG["verbose"]:
        for arg in args:
            print arg,
        print


def send_file(sc, filename, message):
    # Remove formatting if not preformatted
    if message is not None:
        if not CONFIG["formatted"]:
            message = "```%s```" % message
    else:  # TODO: confirm this is required
        message = ""

    # Send the post message request
    with open(filename) as fileobj:
        req = sc.api_call(
            "files.upload",
            channel="#%s" % CONFIG["channel"],
            filename=filename,
            content=fileobj.read()
        )
    vprint("Sending request:\n%s\n" % pprint.pformat(req))


def send_text(sc, message):
    # Remove formatting if not preformatted
    if not CONFIG["formatted"]:
        message = "```%s```" % message

    # Send the post message request
    req = sc.api_call(
        "chat.postMessage",
        channel="#%s" % CONFIG["channel"],
        text=message,
        username=CONFIG["username"],
        icon_emoji=CONFIG["emoji"]
    )
    vprint("Sending request:\n%s\n" % pprint.pformat(req))


def send_stdin(sc):
    # Print each line if reading "live"
    if CONFIG["live"]:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            sys.stdout.write(line)
            send_text(sc, line)

    # Otherwise, buffer until end of stdin
    else:
        message = ""
        for line in sys.stdin:
            sys.stdout.write(line)
            message += line
        send_text(sc, message)


def slackerr():
    # Load configuration from file
    try:
        config_filename = "%s/.slackerr" % os.path.expanduser("~")
        with open(config_filename) as config_file:
            CONFIG.update(json.load(config_file))
    except:
        pass

    # Setup argument parsing
    parser = argparse.ArgumentParser(
        description="Pipe directly to Slack from your shell")
    parser.add_argument("-t", "--token", help="Slack API authentication token")
    parser.add_argument("-c", "--channel",
                        help="specify the channel to send to")
    parser.add_argument("-u", "--username",
                        help="specify the username to send as")
    # parser.add_argument("-f", "--file", help="a file to attach to message")
    # TODO
    parser.add_argument(
        "--formatted", help="assume message is preformatted", action="store_true")
    parser.add_argument(
        "--live", help="actively send from stdin", action="store_true")
    # parser.add_argument("-i", "--interval", help="how often to flush the
    #   live buffer") TODO
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")
    parser.add_argument("message", help="", nargs='?')

    # Parse command line arguments
    args = vars(parser.parse_args())
    message = args.pop("message")
    #filename = args.pop("file")

    # Update configuration and dump
    CONFIG.update({k: v for (k, v) in args.items() if v is not None})
    vprint("Configuration settings:\n%s\n" % pprint.pformat(CONFIG))

    # Ensure a token was provided
    if "token" not in CONFIG or CONFIG["token"] is None:
        print "No Slack API token has been provided"
        sys.exit(-1)

    # Initialize session
    sc = SlackClient(CONFIG["token"])

    # Verify authentication
    auth_test = sc.api_call("auth.test")
    if not auth_test["ok"]:
        print "Slack API error: %s" % auth_test["error"]
        sys.exit(-1)
    vprint(pprint.pformat(auth_test))

    # If a file was provided, send it
    '''
    if filename is not None:
        send_file(sc, filename, message)
    '''

    # If a message was provided, send it
    if message is not None:
        send_text(sc, message)

    # Otherwise, read from stdin
    else:
        send_stdin(sc)

if __name__ == "__main__":
    try:
        slackerr()
    except KeyboardInterrupt:
        pass
