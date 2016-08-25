# slackerr
Pipe directly to Slack from your shell

## Setup
TODO

## Usage

```sh
slackerr [options] [message]
```

Pipe directly to Slack from your shell

### Options
```
  -h, --help            show this help message and exit
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
slackerr --formatted < README.md
```

```sh
tail -f some.log | ./slackerr --live
```

```sh
slackerr --username olanmatt --channel bots "Hello, world!"
```
