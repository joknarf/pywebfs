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
![image](https://github.com/user-attachments/assets/cd123917-9967-48ca-9954-1745dc43f847)

* search text in files (grep)
![image](https://github.com/user-attachments/assets/f0cf4dda-2724-4137-967f-561cd12e60d5)

## features

* Serve static files
* Download folder as zip file
* Filter files
* Search files recursively multiple word any order (disable feature with --nosearch)
* Search text in files recursively
* Basic Auth support (single user)
* HTTPS support
* HTTPS self-signed certificate generator
* Display owner/group/permissions (POSIX) (disable feature with --noperm)
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

## Disclaimer

As built on python http.server, read in the python3 documentation:

>Warning
>http.server is not recommended for production. It only implements basic security checks.
