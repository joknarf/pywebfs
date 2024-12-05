#!/bin/env python
""" HTTP File server class"""
# pylint: disable=C0103

import os
import sys
import re
import argparse
import urllib
import html
from http.server import (
    ThreadingHTTPServer,
    SimpleHTTPRequestHandler,
)
from http import HTTPStatus
import urllib.parse


FOLDER = '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path id="SVGCleanerId_0" style="fill:#FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path> <g> <path id="SVGCleanerId_0_1_" style="fill:#FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path> </g> <path style="fill:#EFF2FA;" d="M485.517,70.621H26.483c-4.875,0-8.828,3.953-8.828,8.828v44.138h476.69V79.448 C494.345,74.573,490.392,70.621,485.517,70.621z"></path> <rect x="17.655" y="105.931" style="fill:#E1E6F2;" width="476.69" height="17.655"></rect> <path style="fill:#FFD782;" d="M494.345,88.276H217.318c-3.343,0-6.4,1.889-7.895,4.879l-10.336,20.671 c-2.99,5.982-9.105,9.76-15.791,9.76H55.05c-6.687,0-12.801-3.778-15.791-9.76L28.922,93.155c-1.495-2.99-4.552-4.879-7.895-4.879 h-3.372C7.904,88.276,0,96.18,0,105.931v335.448c0,9.751,7.904,17.655,17.655,17.655h476.69c9.751,0,17.655-7.904,17.655-17.655 V105.931C512,96.18,504.096,88.276,494.345,88.276z"></path> <path style="fill:#FFC36E;" d="M485.517,441.379H26.483c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h459.034c4.875,0,8.828,3.953,8.828,8.828l0,0C494.345,437.427,490.392,441.379,485.517,441.379z"></path> <path style="fill:#EFF2FA;" d="M326.621,220.69h132.414c4.875,0,8.828-3.953,8.828-8.828v-70.621c0-4.875-3.953-8.828-8.828-8.828 H326.621c-4.875,0-8.828,3.953-8.828,8.828v70.621C317.793,216.737,321.746,220.69,326.621,220.69z"></path> <path style="fill:#C7CFE2;" d="M441.379,167.724h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,163.772,446.254,167.724,441.379,167.724z"></path> <path style="fill:#D7DEED;" d="M441.379,203.034h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,199.082,446.254,203.034,441.379,203.034z"></path> </g></svg>'
FOLDER_CSS = '<svg width="16px" height="16px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="%23000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path id="SVGCleanerId_0" style="fill:%23FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path><g><path id="SVGCleanerId_0_1_" style="fill:%23FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path></g><path style="fill:%23EFF2FA;" d="M485.517,70.621H26.483c-4.875,0-8.828,3.953-8.828,8.828v44.138h476.69V79.448 C494.345,74.573,490.392,70.621,485.517,70.621z"></path><rect x="17.655" y="105.931" style="fill:%23E1E6F2;" width="476.69" height="17.655"></rect><path style="fill:%23FFD782;" d="M494.345,88.276H217.318c-3.343,0-6.4,1.889-7.895,4.879l-10.336,20.671 c-2.99,5.982-9.105,9.76-15.791,9.76H55.05c-6.687,0-12.801-3.778-15.791-9.76L28.922,93.155c-1.495-2.99-4.552-4.879-7.895-4.879 h-3.372C7.904,88.276,0,96.18,0,105.931v335.448c0,9.751,7.904,17.655,17.655,17.655h476.69c9.751,0,17.655-7.904,17.655-17.655 V105.931C512,96.18,504.096,88.276,494.345,88.276z"></path><path style="fill:%23FFC36E;" d="M485.517,441.379H26.483c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h459.034c4.875,0,8.828,3.953,8.828,8.828l0,0C494.345,437.427,490.392,441.379,485.517,441.379z"></path><path style="fill:%23EFF2FA;" d="M326.621,220.69h132.414c4.875,0,8.828-3.953,8.828-8.828v-70.621c0-4.875-3.953-8.828-8.828-8.828 H326.621c-4.875,0-8.828,3.953-8.828,8.828v70.621C317.793,216.737,321.746,220.69,326.621,220.69z"></path><path style="fill:%23C7CFE2;" d="M441.379,167.724h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,163.772,446.254,167.724,441.379,167.724z"></path><path style="fill:%23D7DEED;" d="M441.379,203.034h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,199.082,446.254,203.034,441.379,203.034z"></path></g></svg>'
UPFOLDER_CSS = '<svg width="16px" height="16px" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M12.9998 8L6 14L12.9998 21" stroke="%23000000" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"></path><path d="M6 14H28.9938C35.8768 14 41.7221 19.6204 41.9904 26.5C42.2739 33.7696 36.2671 40 28.9938 40H11.9984" stroke="%23000000" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"></path></g></svg>'
HOME_CSS = '<svg width="16px" height="16px" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M1 6V15H6V11C6 9.89543 6.89543 9 8 9C9.10457 9 10 9.89543 10 11V15H15V6L8 0L1 6Z" fill="%23000000"></path></g></svg>'
FILE_CSS = '<svg width="16px" height="16px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="%23000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M6 10h12v1H6zM3 1h12.29L21 6.709V23H3zm12 6h5v-.2L15.2 2H15zM4 22h16V8h-6V2H4zm2-7h12v-1H6zm0 4h9v-1H6z"></path><path fill="none" d="M0 0h24v24H0z"></path></g></svg>'
LINK_CSS = '<svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M9.16488 17.6505C8.92513 17.8743 8.73958 18.0241 8.54996 18.1336C7.62175 18.6695 6.47816 18.6695 5.54996 18.1336C5.20791 17.9361 4.87912 17.6073 4.22153 16.9498C3.56394 16.2922 3.23514 15.9634 3.03767 15.6213C2.50177 14.6931 2.50177 13.5495 3.03767 12.6213C3.23514 12.2793 3.56394 11.9505 4.22153 11.2929L7.04996 8.46448C7.70755 7.80689 8.03634 7.47809 8.37838 7.28062C9.30659 6.74472 10.4502 6.74472 11.3784 7.28061C11.7204 7.47809 12.0492 7.80689 12.7068 8.46448C13.3644 9.12207 13.6932 9.45086 13.8907 9.7929C14.4266 10.7211 14.4266 11.8647 13.8907 12.7929C13.7812 12.9825 13.6314 13.1681 13.4075 13.4078M10.5919 10.5922C10.368 10.8319 10.2182 11.0175 10.1087 11.2071C9.57284 12.1353 9.57284 13.2789 10.1087 14.2071C10.3062 14.5492 10.635 14.878 11.2926 15.5355C11.9502 16.1931 12.279 16.5219 12.621 16.7194C13.5492 17.2553 14.6928 17.2553 15.621 16.7194C15.9631 16.5219 16.2919 16.1931 16.9495 15.5355L19.7779 12.7071C20.4355 12.0495 20.7643 11.7207 20.9617 11.3787C21.4976 10.4505 21.4976 9.30689 20.9617 8.37869C20.7643 8.03665 20.4355 7.70785 19.7779 7.05026C19.1203 6.39267 18.7915 6.06388 18.4495 5.8664C17.5212 5.3305 16.3777 5.3305 15.4495 5.8664C15.2598 5.97588 15.0743 6.12571 14.8345 6.34955" stroke="%23000000" stroke-width="2" stroke-linecap="round"></path></g></svg>'
SEARCH_CSS = '<svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M16.6725 16.6412L21 21M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="%23000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></g></svg>'

CSS = f"""
    body {{
        margin: 0px;
        padding: 0px;
        background-color: #F3F4FF;
        /*border-radius: 0px 0px 10px 10px;*/
        font-family: verdana, helvetica, arial, sans-serif;
        font-size: 1em;
    }}
    @media screen and (max-device-width: 480px){{
        body{{
            -webkit-text-size-adjust: 150%;
        }}
    }}
    a {{ text-decoration: none; }}
    ul {{ 
        list-style-type: none;
        padding: 10px 20px;
    }}
    form {{ display: inline; }}
    svg {{
        width: 16px;
        height: 16px;
        padding-right: 5px;
    }}
    header {{
        position: fixed;
        top: 0;
        left: 0;
        width: calc(100% - 40px);
        margin: 0px;
        border: 0px;
        /*border-radius: 10px 10px 0px 0px;*/
        background-color: #aaa;
        padding: 10px 20px;
        display: inline-block;
    }}

    main {{
        margin-top: 43px;
    }}
    input {{
        display: inline-block;
        margin-right: 10px;
        vertical-align: center;
    }}
    .search {{
        -webkit-appearance: none;
        -webkit-border-radius: none;
        appearance: none;
        border-radius: 0px;
        height: 25px;
        border: 0px;
        background: url('data:image/svg+xml;utf8,{SEARCH_CSS}') no-repeat;
        background-size: 18px 18px;
        background-position-y: center;
    }}
    .home {{
        display: inline-block;
        text-indent: 25px;
        vertical-align: center;
        background: url('data:image/svg+xml;utf8,{HOME_CSS}') no-repeat;
        background-size: 18px 18px;
        background-position-y: bottom;
    }}

    .folder {{
        display: inline-block;
        text-indent: 20px;
        background: url('data:image/svg+xml;utf8,{FOLDER_CSS}') no-repeat;
        background-size: 16px 16px;
    }}
    .file {{
        display: inline-block;
        text-indent: 20px;
        background: url('data:image/svg+xml;utf8,{FILE_CSS}') no-repeat;
        background-size: 16px 16px;
    }}
    .link {{
        display: inline-block;
        text-indent: 20px;
        background: url('data:image/svg+xml;utf8,{LINK_CSS}') no-repeat;
        background-size: 16px 16px;
    }}
    .upfolder {{
        display: inline-block;
        text-indent: 20px;
        background: url('data:image/svg+xml;utf8,{UPFOLDER_CSS}') no-repeat;
        background-size: 16px 16px;
        width: 100px;
    }}
"""

ENC = sys.getfilesystemencoding()
HTML = f"""
<!DOCTYPE HTML>
<html lang="en">
<head>
<link rel="icon" href="/favicon.svg">
<link rel="stylesheet" href="/style.css">
<meta charset="{ENC}">
"""

# <style>
# {CSS}
# </style>


def accent_re(rexp):
    """ regexp search any accent """
    return (
        rexp.replace("e", "[eéèêë]")
        .replace("a", "[aàäâ]")
        .replace("i", "[iïìî]")
        .replace("c", "[cç]")
        .replace("o", "[oô]")
        .replace("u", "[uùûü]")
    )


class HTTPFileHandler(SimpleHTTPRequestHandler):
    """Class handler for HTTP"""

    def _set_response(self, status_code, data, content_type=None):
        """build response"""

        self.send_response(status_code)
        encoded = data.encode(ENC, "surrogateescape")
        if content_type:
            self.send_header("Content-type", "%s; charset=%s" % (ENC, content_type))
        else:
            self.send_header("Content-type", "text/html; charset=%s" % ENC)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def find_files(self, search, path):
        """ find files recursively with name contains any word in search"""
        r = []
        rexp = []
        err = 0
        for s in search.split():
            try:
                rexp.append(re.compile(accent_re(s), re.IGNORECASE))
            except:
                err = 1
        if err:
            return "<li><b>Invalid regexp in search</b></li></ul></main></body></html>"
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if all([bool(x.search(filename)) for x in rexp]):
                    fpath = os.path.join(dirpath, filename).replace("\\", "/")[1:]
                    r.append(
                        '<li><a href="%s" class="file">%s</a></li>'
                        % (
                            urllib.parse.quote(fpath, errors="surrogatepass"),
                            html.escape(filename, quote=False),
                        )
                    )
        return "\n".join(r)

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        if path != "./":
            r.append(
                f"<li><a href='{urllib.parse.quote(os.path.dirname(path[1:-1]), errors='surrogatepass')}' class='upfolder'>..</a></li>"
            )
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            img = "file"
            if os.path.isdir(fullname):
                linkname = name + "/"
                img = "folder"
            if os.path.islink(fullname):
                img = "link"
            r.append(
                '<li><a href="%s" class="%s">%s</a></li>'
                % (
                    urllib.parse.quote(linkname, errors="surrogatepass"),
                    img,
                    html.escape(displayname, quote=False),
                )
            )
        return "\n".join(r)

    def end_headers(self):
        is_file = "?" not in self.path and not self.path.endswith("/")
        # adds extra headers for some file types.
        if is_file:
            mimetype = self.guess_type(self.path)
            if mimetype in ["text/plain"]:
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Disposition", "inline")
            self.send_header("Cache-Control", "max-age=604800")
        super().end_headers()

    def do_GET(self):
        """do http calls"""
        self.log_message(
            "%s http://%s%s", self.command, self.headers["Host"], self.path
        )
        if self.path == "/favicon.svg":
            return self._set_response(HTTPStatus.OK, FOLDER, "image/svg+xml")
        elif self.path == "/style.css":
            return self._set_response(HTTPStatus.OK, CSS, "text/css")
        elif self.path == "/favicon.ico":
            return self._set_response(HTTPStatus.NOT_FOUND, "")
        p = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(p.query)
        search = q.get("search", [""])[0]
        urllib.parse.urlparse
        try:
            displaypath = urllib.parse.unquote(p.path, errors="surrogatepass")
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(p.path)
        path = displaypath
        displaypath = html.escape(displaypath, quote=False)
        title = f"{self.server.title} - {displaypath}"
        htmldoc = HTML
        htmldoc += f"<title>{title}</title>\n</head>"
        htmldoc += "<body>"

        href = '<a href="/" class="home">/</a>'
        fpath = "/"
        for dir in path.split("/")[1:-1]:
            fpath += dir + "/"
            href += '<a href="%s">%s</a>/' % (
                urllib.parse.quote(fpath, errors="surrogatepass"),
                html.escape(dir, quote=False),
            )
        htmldoc += "<header>"
        # htmldoc += '<div>'
        htmldoc += "<form name=search>"
        htmldoc += f"<input type=text name=search value='{search}' autofocus>"
        #htmldoc += '<a href="javascript:document.forms[\'search\'].submit()" class="search">&nbsp;</a>'
        htmldoc += '<input type=submit value="&nbsp;&nbsp;&nbsp;" class="search">'

        htmldoc += ''
        htmldoc += f"{href}\n</header>"
        htmldoc += "</form>"
        htmldoc += "<main><ul>"

        enddoc = "\n</ul>\n</main></body>\n</html>\n"

        if p.query:
            htmldoc += self.find_files(search, "." + path) + enddoc
            self._set_response(HTTPStatus.OK, htmldoc)
        elif displaypath.endswith("/"):
            htmldoc += self.list_directory("." + path) + enddoc
            self._set_response(HTTPStatus.OK, htmldoc)
        else:
            super().do_GET()


class HTTPFileServer(ThreadingHTTPServer):
    """HTTPServer with httpfile"""

    def __init__(self, title, *args, **kwargs):
        """add title property"""
        self.title = title
        super().__init__(*args, **kwargs)


def main():
    """start http server according to args"""
    parser = argparse.ArgumentParser(prog="pywebfs")
    parser.add_argument(
        "-s", "--server", type=str, default="0.0.0.0", help="HTTP server listen address"
    )
    parser.add_argument(
        "-p", "--port", type=int, default=8080, help="HTTP server listen port"
    )
    parser.add_argument(
        "-d", "--dir", type=str, default=os.getcwd(), help="Serve target directory"
    )
    parser.add_argument(
        "-t",
        "--title",
        type=str,
        default="FileBrowser",
        nargs="?",
        help="Web html title",
    )
    parser.add_argument("-D", "--daemon", action="store_true", help="Start as a daemon")
    args = parser.parse_args()
    if os.path.isdir(args.dir):
        try:
            os.chdir(args.dir)
        except OSError:
            print(f"Error: cannot chdir {args.dir}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: {args.dir} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Starting http server : http://{args.server}:{args.port}")
    server = HTTPFileServer(args.title, (args.server, args.port), HTTPFileHandler)

    if args.daemon:
        import daemon
        daemon_context = daemon.DaemonContext()
        daemon_context.files_preserve = [server.fileno()]
        with daemon_context:
            os.chdir(args.dir)
            server.serve_forever()
    else:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Stopping http server")
            sys.exit(0)


if __name__ == "__main__":
    main()
