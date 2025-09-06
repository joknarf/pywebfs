[![Joknarf Tools](https://img.shields.io/badge/Joknarf%20Tools-Visit-darkgreen?logo=github)](https://joknarf.github.io/joknarf-tools)
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
![image](https://github.com/user-attachments/assets/32f27193-e23f-4aff-b78b-fc58d378f5dd)

* search text in files (like grep -ri)
![image](https://github.com/user-attachments/assets/89bf3f6b-6d7e-4f9c-9b08-20525ba2c670)

## features

* Serve static files
* Download folder as zip file
* Quick filter files
* Keyboard navigation using arrows
* Search files by name recursively with multiple word any order
* Search text in files recursively (disable feature with --nosearch)
* Basic Auth support (single user)
* Safe url token Auth
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

## Safe url token auth
```
$ pywebfs --dir /mydir --tokenurl
$ pywebfs --d /mydir --T
```
A Token is generated, unless PYWEBFS_TOKEN environment variable is set

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
