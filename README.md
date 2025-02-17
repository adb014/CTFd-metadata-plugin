# CTFd Metadata plugin

This plugin allows the CTFd administrator to include metadata in their challenges.
The idea is that this metadata is used by other processes outside of CTFd in a 
complete platform. This metadata appears no where within CTFd itself. The
metadata is stored as a simple string, but typically should use a JSON format for
the complete data

## Installation

1. Clone this repository to [CTFd/plugins](https://github.com/CTFd/CTFd/tree/master/CTFd/plugins).
2. There are no specific python requirements for this package
3. You'll need to restart CTFd after installing the plugin. However, you'll also need to restart if you change the theme, as the challenge html template is only overwritten during the startup of CTFd for the needs of the solution plugin. If you change the theme and do not restart CTFd, the solution plugin will attempt to write to non existent places in the templates and crash.
4. In the `Admin Panel` go to `Plugins` -> `metadata`. There you will find the list of all of the challenges and their metadata
5. Click on the challenge desired and you can add a metadata
