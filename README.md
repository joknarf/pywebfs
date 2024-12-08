[![Pypi version](https://img.shields.io/pypi/v/pywebfs.svg)](https://pypi.org/project/pywebfs/)
![example](https://github.com/joknarf/pywebfs/actions/workflows/python-publish.yml/badge.svg)
[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](https://shields.io/)
[![](https://pepy.tech/badge/pywebfs)](https://pepy.tech/project/pywebfs)
[![Python versions](https://img.shields.io/badge/python-3.6+-blue.svg)](https://shields.io/)

# pywebfs
Simple Python HTTP(S) File Server

# Quick start
```
$ pywebfs -d /mydir -t "my fileserver" -s 0.0.0.0 -p 8080
```
* Browse/Download/Search files using browser `http://<yourserver>:8080`
![image](https://github.com/user-attachments/assets/ebb9957f-5a10-4e71-8db7-ee19dd9ecc7e)

* search text in files (grep)
![image](https://github.com/user-attachments/assets/44134bfb-7e73-46c9-9bee-59fff376e345)

# basic auth
```
$ pywebfs --dir /mydir --user myuser [--password mypass]
$ pywebfs -d /mydir -u myuser [-P mypass]
```
Generated password is given if no `--pasword` option

# https server

* Generate auto-signed certificate and start https server
```
$ pywebfs --dir /mydir --gencert myserver 192.169.1.11
$ pywebfs -d /mydir --g myserver 192.169.1.11
```

* Start https server using existing certificate
```
$ pywebfs --dir /mydir --cert /pathto/host.cert --key /pathto/host.key
$ pywebfs -d /mydir -c /pathto/host.cert -k /pathto/host.key
```
