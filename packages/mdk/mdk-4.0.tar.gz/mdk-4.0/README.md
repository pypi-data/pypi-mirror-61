# mdk

`mdk` is a cli helper for docker built at [Matician](https://matician.com/).

## Prerequisites
* Python (3)
* pip (3)
* Docker(ce)

### About Docker versions
Though `mdk` itself does not require a specific Docker version, it is often used in conjection with Docker features from the 1.40 Docker API. This is only supported by Docker releases >= 19.

## Installation
```sh
$ sudo pip3 install --user mdk
```

Note: you must have the `mdk` executable in your `$PATH`. If you used the installation instructions above, the executable is in `~/.local/bin`.

## Usage
Run the `mdk` command after installation for a full list of commands. For help on individual commands, use `mdk COMMAND --help`.

## FAQ

### How do I add custom configuration to containers created by `mdk`?
`mdk` automatically loads additional options from two files:
* `ext.mdk.json` located in the same directory as `mdk.json`
* `~/.config/mdk/mdk.json`
