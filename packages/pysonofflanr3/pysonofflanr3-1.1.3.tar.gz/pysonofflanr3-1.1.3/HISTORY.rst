History
=======

1.1.2 (2020-02-16)
------------------

* Fixed issue of reconnection that device remains unavailable until state changes
* Fixed retry code for strip type devices


1.1.1 (2020-02-01)
------------------

* Optimisations to deal with later zeroconf versions which have some different behaviour
* Improved error handling of unexpected errors

1.1.0 (2020-01-10)
------------------

* First release on PyPI.
* Forked from PySonoffLAN package (courtesy of Andrew Beveridge)
* Works on V3 Itead firmware using mDNS for service discovery and REST for service invocation
* Supports DIY mode as well as 'standard' mode (for standard mode API key is needed to be obtained, e.g. by sniffing LAN)
* Supports all known devices for switching, although no sensors added at this point
