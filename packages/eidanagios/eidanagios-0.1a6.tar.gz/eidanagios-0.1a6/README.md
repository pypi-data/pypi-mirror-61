Nagios plugins and test code for EIDA services
==============================================

![](https://img.shields.io/pypi/v/eidanagios.svg) ![](https://img.shields.io/pypi/pyversions/eidanagios.svg) ![](https://img.shields.io/pypi/format/eidanagios.svg) ![](https://img.shields.io/pypi/status/eidanagios.svg)

Scripts to check EIDA service from a Nagios system or from the command line.

Overview
--------

This package provides the needed tools to check if different EIDA services are working properly. It follows the standard specification to develop Nagios plugins, but can also be used from the command line as a regular executable.

check_EIDA_auth
---------------
This utility lets you check an EIDA auth endpoint by presenting a token and trying to authenticate.

A typical help message from ``check_EIDA_auth`` looks like the following:

    $ check_EIDA_auth -h
    usage: check_EIDA_auth [-h] [-H HOSTNAME | -u URL] [-t TIMEOUT]
                           [-a AUTHENTICATION] [-V] [-v]
    
    Nagios plugin to check an EIDA auth endpoint. If no arguments are passed all
    EIDA nodes are tested.
    
    optional arguments:
      -h, --help            show this help message and exit
      -H HOSTNAME, --hostname HOSTNAME
                            Hostname providing the "auth" method at the default
                            location. Valid values are domain names (e.g.
                            geofon.gfz-potsdam.de) or the data centre ID (BGR,
                            ETH, GFZ, INGV, KOERI, LMU, NIEP, NOA, ODC, RESIF,
                            UIB)
      -u URL, --url URL     URL pointing to the "auth" method to check. Use with
                            non-standard locations
      -t TIMEOUT, --timeout TIMEOUT
                            Number of seconds to be used as a timeout for the HTTP
                            calls.
      -a AUTHENTICATION, --authentication AUTHENTICATION
                            File containing the token to use during the
                            authentication process
      -V, --version         Show version information.
      -v, --verbose

check_EIDA_alparray
-------------------
This utility lets you check that the Alparray data is available from an EIDA node.

A typical help message from ``check_EIDA_alparray`` looks like the following:

    $ check_EIDA_alparray -h    
    usage: check_EIDA_alparray [-h] [-H HOSTNAME] [-t TIMEOUT] [-a AUTHENTICATION]
                               [-V] [-v]
    
    Nagios plugin to check if Alparray data is accessible from endpoints If no
    arguments are passed all EIDA nodes are tested.
    
    optional arguments:
      -h, --help            show this help message and exit
      -H HOSTNAME, --hostname HOSTNAME
                            Hostname providing the "auth" and "queryauth" method
                            at the default location. Valid values are domain names
                            (e.g. geofon.gfz-potsdam.de) or the data centre ID
                            (ETH, GFZ, INGV, LMU, ODC, RESIF)
      -t TIMEOUT, --timeout TIMEOUT
                            Number of seconds to be used as a timeout for the HTTP
                            calls.
      -a AUTHENTICATION, --authentication AUTHENTICATION
                            File containing the token to use during the
                            authentication process
      -V, --version         Show version information.
      -v, --verbose         If this option is enabled more lines with details will
                            follow the expected one-line message
                        
License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
