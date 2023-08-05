# Escarpolette

This project provides a server and clients to manage your music playlist when you are hosting a party.

It supports many sites thanks to the awesome project [youtube-dl](https://rg3.github.io/youtube-dl/).

## Features

Server:
* add items (and play them!)
* get playlist's items
* runs on Android! (see [instructions](#Android))

Web client:
* there is currently no web client :(

## Dependencies

* Python 3.7
* the player [mpv](https://mpv.io)

They should be available for most of the plateforms.


## Installation

```Shell
pip install escarpolette
```

### Android

You will need [Termux](https://termux.com/).
Then inside Termux you can install it with:

```Shell
# dependencies
pkg install python python-dev clang mpv
# escarpolette
pip install escarpolette
```

Note that while the project can run without wake-lock, acquiring it improve the performance (with a battery trade off).

## Usage

```Shell
escarpolette [--config config.cfg] [--host host] [--port port] [--help]
```

The default configuration should be good for all the usages.

## Dev

You will need [Poetry](https://poetry.eustace.io/) to manage the dependencies.

Clone the repo and then type `poetry install`.
You can run the app with `poetry run python -m escarpolette`.

## Todo

* server
    * votes
    * bonjour / mDNS
    * prevent adding youtube / soundcloud playlists
    * restrictions by users
    * configuration of those restrictions by an admin
* web client
    * show playing status
    * votes
    * configure restrictions:
        * max video added per user
        * max video length
    * admin access:
        * configure restrictions
        * no restrictions for him
        * force video order

Maybe one day?
* android client
* iOS client
