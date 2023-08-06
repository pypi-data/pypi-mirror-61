thumbor_multidir
================

Thumbor file loader that checks multiple paths

Introduction
------------

[Thumbor](https://github.com/globocom/thumbor/wiki) is a smart imaging service. It enables on-demand crop, resizing and flipping of images.

Usage
-----

Using it is simple, just change your configuration in thumbor.conf (or enviroment variable) before running Thumbor:

    # List of paths to check for file to load
    # defaults to empty list which is an error so all requests will return 404
    TC_MULTIDIR_PATHS = ['/home/media', '/mnt/media']

To use tc_multidir for loading original images, change your thumbor.conf or environment variables to read:

    LOADER = 'tc_multidir.loader'

Running Thumbor
---------------

Note: If using environment variables run Thumbor with the `--use-environment` flag or other method to load it into the thumbor.conf template.

See [Thumbor repo](https://github.com/thumbor/thumbor)
or use the Docker container maintaned by [MinimalCompact](https://github.com/MinimalCompact/thumbor/tree/master/thumbor) as a base image... see [/docker/Dockerfile](https://github.com/benneic/thumbor_multidir/tree/master/docker) for an example.
