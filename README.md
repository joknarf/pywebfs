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
![image](https://github.com/user-attachments/assets/d17ae249-71b6-4596-bd37-25022a458276)

* search text in files (grep)
![image](https://github.com/user-attachments/assets/2cb17905-ff55-4773-9c7c-d654c2d2f99f)

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
