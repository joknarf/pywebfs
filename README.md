[![Pypi version](https://img.shields.io/pypi/v/pywebfs.svg)](https://pypi.org/project/pywebfs/)
![example](https://github.com/joknarf/pywebfs/actions/workflows/python-publish.yml/badge.svg)
[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](https://shields.io/)
[![](https://pepy.tech/badge/pywebfs)](https://pepy.tech/project/pywebfs)
[![Python versions](https://img.shields.io/badge/python-3.6+-blue.svg)](https://shields.io/)

# pywebfs
Simple Python HTTP(S) File Server

## Install
```
$ pip install pywebfs
```

## Quick start

* start http server sharing current directory listening on 0.0.0.0 port 8080
```
$ pywebfs
```

* Browse/Download/Search files using browser `http://<yourserver>:8080`
![image](https://github.com/user-attachments/assets/2ef30c9d-5cd9-421a-ab81-12dc2e9ef651)

* search text in files (grep)
![image](https://github.com/user-attachments/assets/2cb17905-ff55-4773-9c7c-d654c2d2f99f)

## features

* Serve static files
* Download folder as zip file
* Filter files
* Search files recursively multiple word any order
* Search text in files recursively
* Basic Auth support (single user)
* HTTPS support
* HTTPS self-signed certificate generator
* Can be started as a daemon (POSIX)

## Customize server
```
$ pywebfs --dir /mydir --title "my fileserver" --listen 0.0.0.0 --port 8080
$ pywebfs -d /mydir -t "my fileserver" -l 0.0.0.0 -p 8080
```

## Basic auth user/password
```
$ pywebfs --dir /mydir --user myuser [--password mypass]
$ pywebfs -d /mydir -u myuser [-P mypass]
```
Generated password is given if no `--pasword` option

## HTTPS server

* Generate auto-signed certificate and start https server
```
$ pywebfs --dir /mydir --gencert
$ pywebfs -d /mydir --g
```

* Start https server using existing certificate
```
$ pywebfs --dir /mydir --cert /pathto/host.cert --key /pathto/host.key
$ pywebfs -d /mydir -c /pathto/host.cert -k /pathto/host.key
```

## Launch server as a daemon (Linux)

```
$ pywebfs start
$ pywebfs status
$ pywebfs stop
```
* log of server are stored in `~/.pywebfs/pwfs_<listen>:<port>.log`