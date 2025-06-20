#!/bin/env python
""" HTTP File server class"""
# pylint: disable=C0103

import os
import sys
import re
import argparse
import urllib
import html
import base64
import unicodedata
from functools import lru_cache
from uuid import uuid4
from secrets import token_urlsafe
# python 3.6 no TheedingHTTPServer
try: 
    from http.server import (
        ThreadingHTTPServer,
        SimpleHTTPRequestHandler,
    )
except:
    from http.server import (
        HTTPServer as ThreadingHTTPServer,
        SimpleHTTPRequestHandler,
    )
from http.cookies import SimpleCookie
from http import HTTPStatus
import ssl
import urllib.parse
from datetime import datetime, timedelta, timezone
from time import sleep
from fnmatch import fnmatchcase
import ipaddress
import secrets
from socket import gethostname, gethostbyname_ex
from shutil import make_archive
try:
    import pwd
    import grp
    NO_PERM = False
except:
    NO_PERM = True
    pass

PYWFSDIR = os.path.expanduser("~/")
if os.path.isdir(f"{PYWFSDIR}/.config"):
    PYWFSDIR += '/.config'
PYWFSDIR += "/.pywebfs"

NO_SEARCH_TXT = False
HIDDEN = [".git", "__pycache__"]

FOLDER = '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path id="SVGCleanerId_0" style="fill:#FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path> <g> <path id="SVGCleanerId_0_1_" style="fill:#FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path> </g> <path style="fill:#EFF2FA;" d="M485.517,70.621H26.483c-4.875,0-8.828,3.953-8.828,8.828v44.138h476.69V79.448 C494.345,74.573,490.392,70.621,485.517,70.621z"></path> <rect x="17.655" y="105.931" style="fill:#E1E6F2;" width="476.69" height="17.655"></rect> <path style="fill:#FFD782;" d="M494.345,88.276H217.318c-3.343,0-6.4,1.889-7.895,4.879l-10.336,20.671 c-2.99,5.982-9.105,9.76-15.791,9.76H55.05c-6.687,0-12.801-3.778-15.791-9.76L28.922,93.155c-1.495-2.99-4.552-4.879-7.895-4.879 h-3.372C7.904,88.276,0,96.18,0,105.931v335.448c0,9.751,7.904,17.655,17.655,17.655h476.69c9.751,0,17.655-7.904,17.655-17.655 V105.931C512,96.18,504.096,88.276,494.345,88.276z"></path> <path style="fill:#FFC36E;" d="M485.517,441.379H26.483c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h459.034c4.875,0,8.828,3.953,8.828,8.828l0,0C494.345,437.427,490.392,441.379,485.517,441.379z"></path> <path style="fill:#EFF2FA;" d="M326.621,220.69h132.414c4.875,0,8.828-3.953,8.828-8.828v-70.621c0-4.875-3.953-8.828-8.828-8.828 H326.621c-4.875,0-8.828,3.953-8.828,8.828v70.621C317.793,216.737,321.746,220.69,326.621,220.69z"></path> <path style="fill:#C7CFE2;" d="M441.379,167.724h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,163.772,446.254,167.724,441.379,167.724z"></path> <path style="fill:#D7DEED;" d="M441.379,203.034h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,199.082,446.254,203.034,441.379,203.034z"></path> </g></svg>'
FOLDER_CSS = '<svg width="16px" height="16px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="%23000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path id="SVGCleanerId_0" style="fill:%23FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path><g><path id="SVGCleanerId_0_1_" style="fill:%23FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path></g><path style="fill:%23EFF2FA;" d="M485.517,70.621H26.483c-4.875,0-8.828,3.953-8.828,8.828v44.138h476.69V79.448 C494.345,74.573,490.392,70.621,485.517,70.621z"></path><rect x="17.655" y="105.931" style="fill:%23E1E6F2;" width="476.69" height="17.655"></rect><path style="fill:%23FFD782;" d="M494.345,88.276H217.318c-3.343,0-6.4,1.889-7.895,4.879l-10.336,20.671 c-2.99,5.982-9.105,9.76-15.791,9.76H55.05c-6.687,0-12.801-3.778-15.791-9.76L28.922,93.155c-1.495-2.99-4.552-4.879-7.895-4.879 h-3.372C7.904,88.276,0,96.18,0,105.931v335.448c0,9.751,7.904,17.655,17.655,17.655h476.69c9.751,0,17.655-7.904,17.655-17.655 V105.931C512,96.18,504.096,88.276,494.345,88.276z"></path><path style="fill:%23FFC36E;" d="M485.517,441.379H26.483c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h459.034c4.875,0,8.828,3.953,8.828,8.828l0,0C494.345,437.427,490.392,441.379,485.517,441.379z"></path><path style="fill:%23EFF2FA;" d="M326.621,220.69h132.414c4.875,0,8.828-3.953,8.828-8.828v-70.621c0-4.875-3.953-8.828-8.828-8.828 H326.621c-4.875,0-8.828,3.953-8.828,8.828v70.621C317.793,216.737,321.746,220.69,326.621,220.69z"></path><path style="fill:%23C7CFE2;" d="M441.379,167.724h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,163.772,446.254,167.724,441.379,167.724z"></path><path style="fill:%23D7DEED;" d="M441.379,203.034h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,199.082,446.254,203.034,441.379,203.034z"></path></g></svg>'
FOLDER_CSS = '<svg viewBox="0 0 1024 1024" class="icon" version="1.1" xmlns="http://www.w3.org/2000/svg" fill="%23000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M853.333333 256H469.333333l-85.333333-85.333333H170.666667c-46.933333 0-85.333333 38.4-85.333334 85.333333v170.666667h853.333334v-85.333334c0-46.933333-38.4-85.333333-85.333334-85.333333z" fill="%23FFA000"></path><path d="M853.333333 256H170.666667c-46.933333 0-85.333333 38.4-85.333334 85.333333v426.666667c0 46.933333 38.4 85.333333 85.333334 85.333333h682.666666c46.933333 0 85.333333-38.4 85.333334-85.333333V341.333333c0-46.933333-38.4-85.333333-85.333334-85.333333z" fill="%23FFCA28"></path></g></svg>'
UPFOLDER_CSS = '<svg width="16px" height="16px" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M12.9998 8L6 14L12.9998 21" stroke="%23000000" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"></path><path d="M6 14H28.9938C35.8768 14 41.7221 19.6204 41.9904 26.5C42.2739 33.7696 36.2671 40 28.9938 40H11.9984" stroke="%23000000" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"></path></g></svg>'
HOME_CSS = '<svg width="16px" height="16px" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M1 6V15H6V11C6 9.89543 6.89543 9 8 9C9.10457 9 10 9.89543 10 11V15H15V6L8 0L1 6Z" fill="%23000000"></path></g></svg>'
FILE_CSS = '<svg width="16px" height="16px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="%23000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M6 10h12v1H6zM3 1h12.29L21 6.709V23H3zm12 6h5v-.2L15.2 2H15zM4 22h16V8h-6V2H4zm2-7h12v-1H6zm0 4h9v-1H6z"></path><path fill="none" d="M0 0h24v24H0z"></path></g></svg>'
LINK_CSS = '<svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M9.16488 17.6505C8.92513 17.8743 8.73958 18.0241 8.54996 18.1336C7.62175 18.6695 6.47816 18.6695 5.54996 18.1336C5.20791 17.9361 4.87912 17.6073 4.22153 16.9498C3.56394 16.2922 3.23514 15.9634 3.03767 15.6213C2.50177 14.6931 2.50177 13.5495 3.03767 12.6213C3.23514 12.2793 3.56394 11.9505 4.22153 11.2929L7.04996 8.46448C7.70755 7.80689 8.03634 7.47809 8.37838 7.28062C9.30659 6.74472 10.4502 6.74472 11.3784 7.28061C11.7204 7.47809 12.0492 7.80689 12.7068 8.46448C13.3644 9.12207 13.6932 9.45086 13.8907 9.7929C14.4266 10.7211 14.4266 11.8647 13.8907 12.7929C13.7812 12.9825 13.6314 13.1681 13.4075 13.4078M10.5919 10.5922C10.368 10.8319 10.2182 11.0175 10.1087 11.2071C9.57284 12.1353 9.57284 13.2789 10.1087 14.2071C10.3062 14.5492 10.635 14.878 11.2926 15.5355C11.9502 16.1931 12.279 16.5219 12.621 16.7194C13.5492 17.2553 14.6928 17.2553 15.621 16.7194C15.9631 16.5219 16.2919 16.1931 16.9495 15.5355L19.7779 12.7071C20.4355 12.0495 20.7643 11.7207 20.9617 11.3787C21.4976 10.4505 21.4976 9.30689 20.9617 8.37869C20.7643 8.03665 20.4355 7.70785 19.7779 7.05026C19.1203 6.39267 18.7915 6.06388 18.4495 5.8664C17.5212 5.3305 16.3777 5.3305 15.4495 5.8664C15.2598 5.97588 15.0743 6.12571 14.8345 6.34955" stroke="%23000000" stroke-width="2" stroke-linecap="round"></path></g></svg>'
SEARCH_CSS = '<svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M16.6725 16.6412L21 21M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="%23000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></g></svg>'

FILTER_CSS = '<svg width="800px" height="800px" viewBox="0 -0.5 25 25" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"/><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"/><g id="SVGRepo_iconCarrier"><path fill-rule="evenodd" clip-rule="evenodd" d="M11.132 9.71395C10.139 11.2496 10.3328 13.2665 11.6 14.585C12.8468 15.885 14.8527 16.0883 16.335 15.065C16.6466 14.8505 16.9244 14.5906 17.159 14.294C17.3897 14.0023 17.5773 13.679 17.716 13.334C18.0006 12.6253 18.0742 11.8495 17.928 11.1C17.7841 10.3573 17.4268 9.67277 16.9 9.12995C16.3811 8.59347 15.7128 8.22552 14.982 8.07395C14.2541 7.92522 13.4982 8.00197 12.815 8.29395C12.1254 8.58951 11.5394 9.08388 11.132 9.71395Z" stroke="%23808080" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M17.5986 13.6868C17.2639 13.4428 16.7947 13.5165 16.5508 13.8513C16.3069 14.1861 16.3806 14.6552 16.7154 14.8991L17.5986 13.6868ZM19.0584 16.6061C19.3931 16.85 19.8623 16.7764 20.1062 16.4416C20.3501 16.1068 20.2764 15.6377 19.9416 15.3938L19.0584 16.6061ZM7.5 12.7499C7.91421 12.7499 8.25 12.4142 8.25 11.9999C8.25 11.5857 7.91421 11.2499 7.5 11.2499V12.7499ZM5.5 11.2499C5.08579 11.2499 4.75 11.5857 4.75 11.9999C4.75 12.4142 5.08579 12.7499 5.5 12.7499V11.2499ZM7.5 15.7499C7.91421 15.7499 8.25 15.4142 8.25 14.9999C8.25 14.5857 7.91421 14.2499 7.5 14.2499V15.7499ZM5.5 14.2499C5.08579 14.2499 4.75 14.5857 4.75 14.9999C4.75 15.4142 5.08579 15.7499 5.5 15.7499V14.2499ZM8.5 9.74994C8.91421 9.74994 9.25 9.41415 9.25 8.99994C9.25 8.58573 8.91421 8.24994 8.5 8.24994V9.74994ZM5.5 8.24994C5.08579 8.24994 4.75 8.58573 4.75 8.99994C4.75 9.41415 5.08579 9.74994 5.5 9.74994V8.24994ZM16.7154 14.8991L19.0584 16.6061L19.9416 15.3938L17.5986 13.6868L16.7154 14.8991ZM7.5 11.2499H5.5V12.7499H7.5V11.2499ZM7.5 14.2499H5.5V15.7499H7.5V14.2499ZM8.5 8.24994H5.5V9.74994H8.5V8.24994Z" fill="%23808080"/></g></svg>'
SEARCH_PLUS_CSS = '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M15.8053 15.8013L21 21M10.5 7.5V13.5M7.5 10.5H13.5M18 10.5C18 14.6421 14.6421 18 10.5 18C6.35786 18 3 14.6421 3 10.5C3 6.35786 6.35786 3 10.5 3C14.6421 3 18 6.35786 18 10.5Z" stroke="%23000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></g></svg>'
SEARCH_TXT_CSS = '<svg width="16px" height="16px" viewBox="6 5 14 14" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path fill-rule="evenodd" clip-rule="evenodd" d="M11.132 9.71395C10.139 11.2496 10.3328 13.2665 11.6 14.585C12.8468 15.885 14.8527 16.0883 16.335 15.065C16.6466 14.8505 16.9244 14.5906 17.159 14.294C17.3897 14.0023 17.5773 13.679 17.716 13.334C18.0006 12.6253 18.0742 11.8495 17.928 11.1C17.7841 10.3573 17.4268 9.67277 16.9 9.12995C16.3811 8.59347 15.7128 8.22552 14.982 8.07395C14.2541 7.92522 13.4982 8.00197 12.815 8.29395C12.1254 8.58951 11.5394 9.08388 11.132 9.71395Z" stroke="%23000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M17.5986 13.6868C17.2639 13.4428 16.7947 13.5165 16.5508 13.8513C16.3069 14.1861 16.3806 14.6552 16.7154 14.8991L17.5986 13.6868ZM19.0584 16.6061C19.3931 16.85 19.8623 16.7764 20.1062 16.4416C20.3501 16.1068 20.2764 15.6377 19.9416 15.3938L19.0584 16.6061ZM7.5 12.7499C7.91421 12.7499 8.25 12.4142 8.25 11.9999C8.25 11.5857 7.91421 11.2499 7.5 11.2499V12.7499ZM5.5 11.2499C5.08579 11.2499 4.75 11.5857 4.75 11.9999C4.75 12.4142 5.08579 12.7499 5.5 12.7499V11.2499ZM7.5 15.7499C7.91421 15.7499 8.25 15.4142 8.25 14.9999C8.25 14.5857 7.91421 14.2499 7.5 14.2499V15.7499ZM5.5 14.2499C5.08579 14.2499 4.75 14.5857 4.75 14.9999C4.75 15.4142 5.08579 15.7499 5.5 15.7499V14.2499ZM8.5 9.74994C8.91421 9.74994 9.25 9.41415 9.25 8.99994C9.25 8.58573 8.91421 8.24994 8.5 8.24994V9.74994ZM5.5 8.24994C5.08579 8.24994 4.75 8.58573 4.75 8.99994C4.75 9.41415 5.08579 9.74994 5.5 9.74994V8.24994ZM16.7154 14.8991L19.0584 16.6061L19.9416 15.3938L17.5986 13.6868L16.7154 14.8991ZM7.5 11.2499H5.5V12.7499H7.5V11.2499ZM7.5 14.2499H5.5V15.7499H7.5V14.2499ZM8.5 8.24994H5.5V9.74994H8.5V8.24994Z" fill="%23000000"></path></g></svg>'
SEARCH_TXT_CSS = '<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" fill="%23000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><g id="Layer_2" data-name="Layer 2"><g id="Icons"><g><rect width="48" height="48" fill="none"></rect><path d="M29,27H13a2,2,0,0,1,0-4H29a2,2,0,0,1,0,4ZM13,31a2,2,0,0,0,0,4h8a2,2,0,0,0,0-4Zm24-5a2,2,0,0,0-2,2V42H7V8H17a2,2,0,0,0,0-4H5A2,2,0,0,0,3,6V44a2,2,0,0,0,2,2H37a2,2,0,0,0,2-2V28A2,2,0,0,0,37,26Zm7.4-.6a1.9,1.9,0,0,1-2.8,0l-5.1-5.1h0A10.4,10.4,0,0,1,31,22a10.1,10.1,0,0,1-7.1-3H13a2,2,0,0,1,0-4h8.5a9.9,9.9,0,0,1-.5-3,10,10,0,0,1,20,0,10.4,10.4,0,0,1-1.6,5.5h-.1l5.1,5.1A1.9,1.9,0,0,1,44.4,25.4ZM27.5,15a.9.9,0,0,1,1-1h4V13h-3a2,2,0,0,1-2-2V10a2,2,0,0,1,2-2H30V6.1a6,6,0,0,0,0,11.8V16H28.5A.9.9,0,0,1,27.5,15ZM37,12a6,6,0,0,0-5-5.9V8h1.5a.9.9,0,0,1,1,1,.9.9,0,0,1-1,1h-4v1h3a2,2,0,0,1,2,2v1a2,2,0,0,1-2,2H32v1.9l1.6-.5.6-.3a.1.1,0,0,1,.1-.1l.7-.5a.1.1,0,0,1,.1-.1l.6-.6h0l.5-.8h0l.2-.4A5.5,5.5,0,0,0,37,12Z"></path></g></g></g></g></svg>'
DOWNLOAD_CSS = '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M12.5535 16.5061C12.4114 16.6615 12.2106 16.75 12 16.75C11.7894 16.75 11.5886 16.6615 11.4465 16.5061L7.44648 12.1311C7.16698 11.8254 7.18822 11.351 7.49392 11.0715C7.79963 10.792 8.27402 10.8132 8.55352 11.1189L11.25 14.0682V3C11.25 2.58579 11.5858 2.25 12 2.25C12.4142 2.25 12.75 2.58579 12.75 3V14.0682L15.4465 11.1189C15.726 10.8132 16.2004 10.792 16.5061 11.0715C16.8118 11.351 16.833 11.8254 16.5535 12.1311L12.5535 16.5061Z" fill="%231C274C"></path><path d="M3.75 15C3.75 14.5858 3.41422 14.25 3 14.25C2.58579 14.25 2.25 14.5858 2.25 15V15.0549C2.24998 16.4225 2.24996 17.5248 2.36652 18.3918C2.48754 19.2919 2.74643 20.0497 3.34835 20.6516C3.95027 21.2536 4.70814 21.5125 5.60825 21.6335C6.47522 21.75 7.57754 21.75 8.94513 21.75H15.0549C16.4225 21.75 17.5248 21.75 18.3918 21.6335C19.2919 21.5125 20.0497 21.2536 20.6517 20.6516C21.2536 20.0497 21.5125 19.2919 21.6335 18.3918C21.75 17.5248 21.75 16.4225 21.75 15.0549V15C21.75 14.5858 21.4142 14.25 21 14.25C20.5858 14.25 20.25 14.5858 20.25 15C20.25 16.4354 20.2484 17.4365 20.1469 18.1919C20.0482 18.9257 19.8678 19.3142 19.591 19.591C19.3142 19.8678 18.9257 20.0482 18.1919 20.1469C17.4365 20.2484 16.4354 20.25 15 20.25H9C7.56459 20.25 6.56347 20.2484 5.80812 20.1469C5.07435 20.0482 4.68577 19.8678 4.40901 19.591C4.13225 19.3142 3.9518 18.9257 3.85315 18.1919C3.75159 17.4365 3.75 16.4354 3.75 15Z" fill="%231C274C"></path></g></svg>'
SORT_CSS = '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M16 18L16 6M16 6L20 10.125M16 6L12 10.125" stroke="%231C274C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M8 6L8 18M8 18L12 13.875M8 18L4 13.875" stroke="%231C274C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></g></svg>'
CSS = f"""
    html, body {{
        padding: 0px;
        margin: 0px;
    }}
    body {{
        background-color: #333;
        font-family: -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;;
        font-size: 1em;
    }}
    pre {{
        margin: 0;
        line-height: 105%
    }}
    table  {{
        /*width: 100%;*/
        border-spacing: 0px;
        border-radius: 10px;
        background-color: #eee;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.50);
        margin: 1px 10px 5px 5px;
    }}
    thead {{
        position: sticky;
        top: 0;
        z-index: 2;
    }}

    tbody tr > td {{
        background-color: #eee;
        z-index: 3;
    }}
    tbody > tr:hover > td {{
        background-color: #ddd;
    }}
    tbody > tr:hover > td:first-child {{
        border-bottom-left-radius: 15px;
        border-top-left-radius: 15px;
    }}
    tbody > tr:hover > td:last-child {{
        border-bottom-right-radius: 15px;
        border-top-right-radius: 15px;
    }}
    tbody > tr:last-child > td:first-child {{
        border-bottom-left-radius: 15px;
    }}
    tbody > tr:last-child > td:last-child {{
        border-bottom-right-radius: 15px;
    }}
    thead > tr > td {{
        background-color:#eee;
    }}
    td, th {{
        white-space: nowrap;
        line-height: 120%;
        padding-right: 10px;
    }}
    th {{
        padding: 5px 5px 2px 0px;
        text-align: left;
        font-weight: unset;
        color: #5c5c5c;
        cursor: pointer;
        background-color: #333;
    }}
    th.size {{
        text-align: right;
    }}
    tr td:first-child a {{
        color: #0366d6;
        padding: 3px 0px 3px 10px;
        width: 100%;
    }}
    #files tr td a:focus {{
        outline: none;
        background-color: #ccf;
        border-radius: 15px;
    }}
    #files tr td:first-child {{
        font-size: 1em;
        padding-right: 15px;
    }}
    #files tr td {{
        font-size: 0.9em;
    }}
    /* size num */
    #files tr td:nth-child(3), #files tr th:nth-child(3) {{
        padding-right: 0px;
        text-align: right;
    }}
    /* unit */
    #files tr td:nth-child(4), #files tr th:nth-child(4) {{
        padding-left: 5px;
    }}
    /* download */
    #files tr td:last-child a {{
        background: url('data:image/svg+xml;utf8,{DOWNLOAD_CSS}') no-repeat;
        display: inline-block;
        text-indent: 20px;
        background-size: 16px 16px;
        cursor: pointer;
    }}    
    #files tr td {{
        font-variant-numeric: tabular-nums;    
    }}
    th.header {{
        padding: 0;
    }}
    div.header {{
        background-color: #aaa;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px 10px 10px;
        display: flex;
        line-height: 120%;
    }}
    #mask {{
        width: 100%;
        margin: 0px;
        padding: 0px 30px 0px 0px;
        background-color: #333;
        z-index: 1;
        top: 0px;
        left: 0px;
        position: sticky;
        display: flex;
    }}
    #list {{
        width: calc(100% - 20px);
        margin: 0px 0px 10px 0px;
        background-color: #F3F4FF;
        border-radius: 0px 10px 10px 10px;
        z-index: 3;
        display: table;
    }}
    a {{ text-decoration: none; }}
    form {{
        display: inline;
    }}
    svg {{
        width: 16px;
        height: 16px;
        padding-right: 5px;
    }}
    input, button {{
        display: inline-block;
        margin-right: 10px;
        vertical-align: middle;
    }}
    input {{
        -webkit-appearance: none;
        -webkit-border-radius: none;
        appearance: none;
        border-radius: 15px;
        padding: 3px;
        padding-right: 13px;
        border: 1px #eee solid;
        height: 15px;
        font-size: 15px;
        outline: none;
        text-indent: 10px;
        background-color: white;
    }}
    #search {{
        background-image: url('data:image/svg+xml;utf8,{FILTER_CSS}');
        background-repeat:  no-repeat;
        background-size: 23px 23px;
        background-position-y: center;
        background-position-x: right;
        text-indent: 7px;
    }}
    .search {{
        background: url('data:image/svg+xml;utf8,{SEARCH_PLUS_CSS}') no-repeat;
    }}
    .searchtxt {{
        background: url('data:image/svg+xml;utf8,{SEARCH_TXT_CSS}') no-repeat;
    }}
    .search, .searchtxt {{
        -webkit-appearance: none;
        -webkit-border-radius: none;
        appearance: none;
        border-radius: 0px;
        height: 25px;
        border: 0px;
        background-size: 18px 18px;
        background-position-y: center;
        cursor: pointer;
        width: 25px;
    }}
    .path {{
        vertical-align: middle;
        color: #000;
    }}
    a.path:hover {{
        color: white;
    }}

    .home {{
        display: inline-block;
        text-indent: 25px;
        vertical-align: middle;
        background: url('data:image/svg+xml;utf8,{HOME_CSS}') no-repeat;
        background-size: 18px 18px;
        background-position-y: 70%;
    }}
    
    .folder {{
        background: url('data:image/svg+xml;utf8,{FOLDER_CSS}') no-repeat;
    }}
    .file {{
        background: url('data:image/svg+xml;utf8,{FILE_CSS}') no-repeat;
    }}
    .link {{
        background: url('data:image/svg+xml;utf8,{LINK_CSS}') no-repeat;
    }}
    .upfolder {{
        background: url('data:image/svg+xml;utf8,{UPFOLDER_CSS}') no-repeat;
        width: 100px;
    }}
    .rootfolder {{
        background: url('data:image/svg+xml;utf8,{HOME_CSS}') no-repeat;
    }}
    .sort {{
        background: url('data:image/svg+xml;utf8,{SORT_CSS}') no-repeat;
        text-indent: 15px !important;
    }}
    .folder, .file, .link, .upfolder, .rootfolder, .sort {{
        display: inline-block;
        text-indent: 20px;
        background-size: 16px 16px;
    }}
    .folder, .file, .link, .upfolder, .rootfolder {{
        background-position-x: 8px;
        background-position-y: 50%;
    }}

    .found {{
        background: #bfc;
    }}
    #info {{
        visibility: hidden;
        position: absolute;
    }}
    tr.titles th {{
        background-color: #d5d5d5;
        width: 1px;
    }}
    th.name {{
        min-width: 150px;
        padding-left: 10px;
    }}
    #files th.name {{
        min-width: 200px;
    }}
    table.searchresult tr td {{
        vertical-align: top;
    }}  
    div.name {{
        float: left;
    }}
    .info {{
        float: right;
        font-size: 0.8em;
        position: relative;
        top: 1px;
    }}
    .form-container {{
        margin: 10% auto;
        padding: 10px;
        display: block;
        width:500px;
        text-align:center;
        background: #eee;
        border-radius: 10px;

        input {{
            margin-bottom: 10px;
        }}
        #login {{
            height: 25px;
        }}
    }}

    @media screen and (max-device-width: 480px){{
        body {{
            -webkit-text-size-adjust: 180%;
        }}
        .search, .searchtxt, .home, .folder, .file, .link, .upfolder, .rootfolder, #files tr td:last-child a {{
            background-size: 32px 32px;
            text-indent: 40px;
        }}
    }}

"""

ENC = sys.getfilesystemencoding()
HTML = """
<!DOCTYPE HTML>
<html lang="en">
<head>
  <meta charset="{charset}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/style.css">
  <title>{title}</title>
</head>
"""
# <link rel="stylesheet" href="/style.css">
# <style>
# {CSS}
# </style>

LOGIN = """
<body>
<div class="form-container">
  <h2>{title}</h2>
  <form method="post" action="/login">
    <input #username type="text" name="username" placeholder="Username" autofocus tabindex="1">
    <br />
    <input #password type="password" name="password" placeholder="Password">
    <br />
    <input type="submit" id="login" value="Login">
    <br />
  </form>
</div>
</body>
"""

JAVASCRIPT = """
    // update nb files/total size
    function updateinfo() {
        document.getElementById("nameinfo").innerHTML=document.getElementById("info").innerHTML;
    }
    // update info on load
    function pywonload() {
        updateinfo();
    }
    window.onload = pywonload;

    // compare function for sorting
    const getCellValue = (tr, idx) => tr.children[idx].title || tr.children[idx].innerText || tr.children[idx].textContent;
    const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
        v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
        )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

    // sort table by clicking on the header
    document.querySelectorAll('tr.titles th').forEach(th => th.addEventListener('click', (() => {
        const table = th.closest('table');
        uprow = table.rows[2]
        const tbody = table.querySelector('tbody');
        table.style.display = 'none';
        Array.from(table.querySelectorAll('tbody tr:nth-child(n+1)'))
            .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
            .forEach(tr => tbody.appendChild(tr) );
        if (['.', '..'].includes(uprow.cells[0].textContent))
            tbody.insertBefore(uprow, table.rows[2]);
        table.style.display = '';
    })));

    previousFilter = '';
    filesTable = document.getElementById("files");
    if (filesTable) {
        lastRow = filesTable.rows.length - 1;
        firstRow = 2;
        focusRow(2)
        setTimeout(() => {
            window.scrollTo(0, 0);
        }, 40);
    }
    // quick filter table
    document.getElementById("search").addEventListener("keyup", function() {
        var input = document.getElementById("search").value.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        if (input == previousFilter) return;
        previousFilter = input;
        if (!filesTable) return;
        rows = filesTable.rows;
        filesTable.style.display = "none";
        rows[lastRow].children[0].style.borderBottomLeftRadius = "";
        rows[lastRow].lastElementChild.style.borderBottomRightRadius = "";
        for (var i = 2; i <rows.length ; i++) {
            var cell = rows[i].children[0];
            if (cell.innerText.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes(input)) {
                if (!firstRow) firstRow = i;
                rows[i].style.display = "";
                lastRow = i;
            } else {
                rows[i].style.display = "none";
            }
        }
        rows[lastRow].children[0].style.borderBottomLeftRadius = "15px";
        rows[lastRow].lastElementChild.style.borderBottomRightRadius = "15px";
        filesTable.style.display = "";
    });

    function focusRow(rowIndex) {
        anchor = filesTable.rows[rowIndex].querySelector('a');
        anchor.focus();
        path = document.getElementById("file");
        if(! [".",".."].includes(anchor.innerHTML)) {
            href = anchor.getAttribute("href")
            path.href = href
            path.textContent = "/" + decodeURIComponent(href);
        }else{
            path.href = "";
            path.innerHTML = "";
        }
    }

    function focusFile(event, table, start, increment, nb) {
        event.preventDefault();
        nbRows = 0;
        for (i = start; i > 1 && i<table.rows.length; i+=increment) {
            if (table.rows[i].style.display !== 'none') {
                nbRows++;
                if (nbRows == nb || i == lastRow || i == firstRow) {
                    focusRect = table.rows[i].getBoundingClientRect();
                    bottomHeader = table.tHead.getBoundingClientRect().bottom;
                    if (focusRect.top < bottomHeader)
                        window.scrollBy(0, focusRect.top-bottomHeader);
                    if (focusRect.bottom > window.innerHeight-focusRect.height)
                        window.scrollBy(0, focusRect.bottom-window.innerHeight+focusRect.height);
                    focusRow(i);
                    return;
                }
            }
        }
        if (start < 2)  start = 2;
        if (start <= lastRow)
            focusRow(start);
    }

    // keyboard navigation
    document.addEventListener('keydown', function(event) {
        if (['Enter', 'Tab'].includes(event.key)) return;
        const focusedElement = document.activeElement;
        const table = document.querySelector('table');

        if (document.activeElement.tagName === 'BODY') rowIndex = 2;
        else rowIndex = focusedElement.closest('tr').rowIndex;
        if (focusedElement.tagName === 'A') {
            if (event.key === 'ArrowRight') {
                event.preventDefault();
                focusedElement.click();
                return;
            }
            if (event.key === 'ArrowLeft') {
                event.preventDefault();
                window.history.back();
                return;
            }
        }
        if (rowIndex == 0) rowIndex = 1;
        if (event.key === 'ArrowUp') return focusFile(event, table, rowIndex-1, -1, 1);
        if (event.key === 'ArrowDown') return focusFile(event, table, rowIndex+1, 1, 1);
        if (event.key === 'End') return focusFile(event, table, lastRow, -1, 1);
        if (event.key === 'Home') return focusFile(event, table, firstRow, 1, 1);
        pageHeight = Math.floor(window.innerHeight/table.rows[2].clientHeight-2);
        if (event.key === 'PageUp') return focusFile(event, table, rowIndex-1, -1, pageHeight);
        if (event.key === 'PageDown') return focusFile(event, table, rowIndex+1, 1, pageHeight);
        document.getElementById("search").focus();
    });

    function dl(hr) {
        document.location.href = hr.parentNode.parentNode.cells[0].firstChild.href + "?download=1";
    }
"""
#JAVASCRIPT=f"<script>\n{JAVASCRIPT}\n</script>"
RE_AGENT = re.compile(r"(Edg|Chrome|Safari|Firefox|Opera|Lynx)[^ ]*")
RE_ACCENT = re.compile(r"[\u0300-\u036f]")

class BadStat:
    st_size = 0
    st_mtime = 0
    st_mode = 0

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

def fs_path(path):
    """ unquote path and convert to filesystem encoding """
    try:
        return urllib.parse.unquote(path, errors="surrogatepass")
    except UnicodeDecodeError:
        return urllib.parse.unquote(path)


def convert_size(size_bytes):
    """ convert size in bytes to human readable """
    if size_bytes == 0:
        return ("0","B")

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    double_size = float(size_bytes)
    while double_size >= 1000 and i < len(size_name) - 1:
        double_size /= 1024.0
        i += 1

    return (str(round(double_size,1)), size_name[i])


def convert_mode(st_mode):
    """ convert mode to rwxrwxrwx """
    permissions = ''
    for i in range(9):
        permissions += ('rwxrwxrwx'[i] if (st_mode & (0o400 >> i)) else '-')
    return permissions

@lru_cache(maxsize=128)
def get_username(uid):
    """get username from uid"""
    if NO_PERM:
        return None
    try:
        return pwd.getpwuid(uid).pw_name
    except KeyError:
        return None

@lru_cache(maxsize=128)
def get_groupname(gid):
    """get groupname from gid"""
    if NO_PERM:
        return None
    try:
        return grp.getgrgid(gid).gr_name
    except KeyError:
        return None


def os_stat(path):
    try:
        return os.stat(path)
    except OSError:
        return BadStat()


def is_binary_file(path):
    if not os.path.isfile(path):
        return None
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    try:
        with open(path, "rb") as fd:
            bytes = fd.read(1024)
        return bool(bytes.translate(None, textchars))
    except PermissionError:
        return True
    
def grep(rex, path, first=False):
    if is_binary_file(path) != False:
        return []
    founds = []
    with open(path, "r", buffering=8192) as fd:
        try:
            for line in fd:
                line = line.rstrip("\r\n")
                found = rex.search(line)
                if found:
                    newline = ""
                    prevspan = 0
                    for m in rex.finditer(line):
                        span = m.span()
                        newline += html.escape(line[prevspan:span[0]]) + '<span class="found">' + html.escape(line[span[0]:span[1]]) + "</span>"
                        prevspan = span[1]
                    newline += html.escape(line[prevspan:])
                    founds.append(newline)
                    if first:
                        return founds
        except Exception as e:
            pass
    return founds

def resolve_hostname(host):
    """try get fqdn from DNS"""
    try:
        return gethostbyname_ex(host)[0]
    except OSError:
        return host

def generate_selfsigned_cert(hostname, ip_addresses=None, key=None):
    """Generates self signed certificate for a hostname, and optional IP addresses.
    from: https://gist.github.com/bloodearnest/9017111a313777b9cce5
    """
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    
    # Generate our key
    if key is None:
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
    
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, hostname)
    ])
 
    # best practice seem to be to include the hostname in the SAN, which *SHOULD* mean COMMON_NAME is ignored.    
    alt_names = [x509.DNSName(hostname)]
    alt_names.append(x509.DNSName("localhost"))
    
    # allow addressing by IP, for when you don't have real DNS (common in most testing scenarios 
    if ip_addresses:
        for addr in ip_addresses:
            # openssl wants DNSnames for ips...
            alt_names.append(x509.DNSName(addr))
            # ... whereas golang's crypto/tls is stricter, and needs IPAddresses
            # note: older versions of cryptography do not understand ip_address objects
            alt_names.append(x509.IPAddress(ipaddress.ip_address(addr)))
    san = x509.SubjectAlternativeName(alt_names)
    
    # path_len=0 means this cert can only sign itself, not other certs.
    basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(1000)
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=10*365))
        .add_extension(basic_contraints, False)
        .add_extension(san, False)
        .sign(key, hashes.SHA256(), default_backend())
    )
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return cert_pem, key_pem

def hidden(name):
    for pat in HIDDEN:
        if fnmatchcase(name, pat):
            return True
    return False

def file_head():
    fields = [
        '<th class="name"><div class="name sort">Name</div><div class="info" id="nameinfo">loading</div></th>',
        '<th><span class="sort">Ext</span></th>',
        '<th class="size"><span class="sort">Size</span></th>',
        '<th></th>',
        '<th>Owner</th>',
        '<th>Group</th>',
        '<th>Perm</th>',
        '<th><span class="sort">Modified</span></th>',
        '<th style=width:100%></th>',
    ]
    if NO_PERM:
        fields = fields[:4] + fields[7:]
    return '<tr class="titles">\n  ' + "\n  ".join(fields) + "\n</tr>\n"

def file_folderup(path):
    """build folder up row"""
    if path == "./":
        scan = os_scandir("./")
        stat = os_stat("./")
        folder = "."
        classname = "rootfolder"
    else:
        folder = ".."
        parentdir = os.path.dirname(path[1:].rstrip("/")).rstrip("/") + "/"
        scan = os_scandir("."+parentdir)
        stat = os_stat("."+parentdir)
        classname = "upfolder"
    fields = [
        f'<td><a href="../" class="{classname}">{folder}</a></td>',
        '<td></td>',
        '<td>%s</td>' % len(tuple(scan)),
        '<td>items</td>',
        '<td>%s</td>' % get_username(stat.st_uid),
        '<td>%s</td>' % get_groupname(stat.st_gid),
        '<td>%s</td>' % convert_mode(stat.st_mode),
        '<td>%s</td>' % datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        '<td></td>',
    ]
    if NO_PERM:
        fields = fields[:4] + fields[7:]
    return "<tr>\n  " + "  \n".join(fields) + "</tr>"

def os_scandir(path):
    """scan directory"""
    try:
        return os.scandir(path)
    except:
        return []

class HTTPFileHandler(SimpleHTTPRequestHandler):
    """Class handler for HTTP"""

    def send_data(self, data):
        """build response"""
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", self.guess_type(self.path))
        self.send_header("Cache-Control", "max-age=3600")
        self.end_headers()
        self.write_html(data)

    def finish(self):
        """finish connection"""
        try:
            return super().finish()
        except ConnectionResetError:
            pass

    def mime_header(self):
        """build header guessing mimetype"""
        mimetype = self.guess_type(self.path)
        fpath = self.translate_path(self.path)
        if mimetype == "application/octet-stream" and is_binary_file(fpath) == False:
            mimetype = "text/plain"
        #self.log_message(mimetype)
        if mimetype in ["text/plain"]:
            self.send_header("Content-Disposition", "inline")
        self.send_header("Content-Type", mimetype)
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

    def file_tr(self, entry, link=None):
        """build file row"""
        if hidden(entry.name):
            return False, 0
        displayname = linkname = entry.name
        if link:
            linkname = link.replace("\\", "/")
        dispsize = ""
        unit = ""
        ext = ""
        stat = entry.stat()
        file = False
        size = 0
        if entry.is_symlink():
            img = "link"
            fsize = 0
            if entry.is_dir():
                linkname += "/"
            else:
                ext = os.path.splitext(displayname)[1][1:] or " "
                displayname = os.path.splitext(displayname)[0]
        elif entry.is_dir():
            linkname += "/"
            img = "folder"
            dispsize = len(tuple(os_scandir(entry.path)))
            fsize = f"-{dispsize}"
            unit = "items"
        else:
            img = "file"
            file = True
            fsize = stat.st_size
            size = stat.st_size
            dispsize, unit = convert_size(stat.st_size)
            ext = os.path.splitext(displayname)[1][1:] or " "
            displayname = os.path.splitext(displayname)[0]
        linkname = urllib.parse.quote(linkname, errors="surrogatepass")
        fields = [
            '<td><a href="%s" class="%s">%s</a></td>' % (linkname, img, html.escape(displayname, quote=False)),
            '<td>%s</td>' % html.escape(ext, quote=False),
            '<td title="%s">%s</td>' % (fsize, dispsize),
            '<td>%s</td>' % unit,
            '<td>%s</td>' % get_username(stat.st_uid),
            '<td>%s</td>' % get_groupname(stat.st_gid),
            '<td>%s</td>' % convert_mode(stat.st_mode),
            '<td>%s</td>' % datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            '<td>%s</td>' % f'<a onclick=dl(this)>&nbsp;</a>',
        ]
        if NO_PERM:
            fields = fields[:4] + fields[7:]
        self.write_html("<tr>\n  " + "\n  ".join(fields) + "\n</tr>\n")
        return file, size

    def find_walk(self, path, rexp, lenpath, infos):
        """find files recursively"""
        for entry in os_scandir(path):
            if hidden(entry.name):
                continue
            if entry.is_dir(follow_symlinks=False):
                self.find_walk(entry.path, rexp, lenpath, infos)
            if all([bool(x.search(entry.name)) for x in rexp]):
                file, size = self.file_tr(entry, entry.path[lenpath:])
                infos[0] += file
                infos[1] += size
        return infos
            
    def find_files(self, search, path):
        """ find files recursively with name contains any word in search"""
        rexp = []
        for s in search.split():
            try:
                rexp.append(re.compile(accent_re(s), re.IGNORECASE))
            except:
                rexp.append(re.compile(accent_re(re.escape(s))))
        self.write_html('<table id="files">\n<thead>\n')
        self.write_html(self.header)
        self.write_html(file_head())
        self.write_html('</thead>\n<tbody>\n')
        nbfiles, size = self.find_walk(path, rexp, len(path), [0,0])
        self.write_html("</tbody>\n</table>\n")
        s = "s" if nbfiles>1 else ""            
        self.write_html(f'<p id="info">{nbfiles} file{s} - {" ".join(convert_size(size))}</p>')

    def search_walk(self, path, rex, lenpath, infos):
        """search recursively in files"""
        for entry in os_scandir(path):
            if hidden(entry.name):
                continue
            if entry.is_dir(follow_symlinks=False):
                self.search_walk(entry.path, rex, lenpath, infos)
            else:
                path = entry.path.replace("\\", "/")
                found = grep(rex, path, first=False)
                if found:
                    infos[0] += 1
                    infos[1] += entry.stat().st_size
                    urlpath = urllib.parse.quote(path[1:], errors="surrogatepass")
                    self.write_html('''
                        <tr>
                            <td><a href="%s" class="file" title="%s">%s</a></td>
                            <td><pre>%s</pre></td>
                            <td></td>
                        </tr>
                        '''
                        % (
                            urlpath,
                            urlpath,
                            html.escape(entry.name, quote=False),
                            "\n".join(found)
                        )
                    )
        return infos

    def search_files(self, search, path):
        """ find files recursively containing search pattern"""
        try:
            rex = re.compile(accent_re(search), re.IGNORECASE)
        except:
            rex = re.compile(accent_re(re.escape(search)), re.IGNORECASE)
        self.write_html('<table class="searchresult">')
        self.write_html('<thead>\n')
        self.write_html(self.header)
        self.write_html('<tr class="titles"><th class="name"><div class="name">Name</div><div class="info" id="nameinfo">loading</div></th><th>Text</th><th style=width:100%></th></tr>')
        self.write_html('</thead>\n<tbody>\n')
        nbfiles, size = (0, 0)
        if search:
            nbfiles, size = self.search_walk(path, rex, len(path), [0,0])
        self.write_html('</tbody>\n</table>')
        s = "s" if nbfiles>1 else ""
        self.write_html(f'<p id="info">{nbfiles} file{s} - {" ".join(convert_size(size))}</p>')
    
    def write_html(self, data):
        """write html data"""
        encoded = data.encode(ENC, "surrogateescape")
        try: 
            self.wfile.write(encoded)
        except:
            pass

    def list_directory(self, path):
        """scandir directory and write html"""
        self.write_html('<table id="files">\n<thead>\n')
        self.write_html(self.header)
        self.write_html(file_head())
        self.write_html(f'</thead>\n<tbody>\n')
        self.write_html(file_folderup(path))
        try:
            entries = os_scandir(path)
        except OSError:
            self.write_html("<tr><td>No permission to list directory</td></tr>")
            self.write_html("</tbody></table>\n")
            self.write_html('<p id="info">0 file - 0 B</p>\n')
            return
        entries = sorted(entries, key=lambda entry: (
            not entry.is_dir(), 
            RE_ACCENT.sub("", unicodedata.normalize("NFD", entry.name.lower()))
        ))
        nbfiles = 0
        size = 0
        for entry in entries:
            file, fsize = self.file_tr(entry)
            size += fsize
            nbfiles += file
        self.write_html("</tbody>\n</table>\n")
        s = "s" if nbfiles>1 else ""
        self.write_html(f'<p id="info">{nbfiles} file{s} - {" ".join(convert_size(size))}</p>\n')

    def download(self, path, inline=False):
        """download file"""
        if os.path.isdir(path):
            tmpdir = os.path.expanduser("~/.pywebfs")
            basedir = os.path.basename(path.rstrip("/"))
            tmpzip = tmpdir + "/" + basedir
            make_archive(tmpzip, 'zip', path,)
            tmpzip += ".zip"
            fstat = os_stat(tmpzip)
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "application/zip")
            self.send_header("Content-Length", str(fstat[6]))
            self.send_header("Content-Disposition", f'attachment; filename="{basedir}.zip"')
            self.end_headers()
            with open(tmpzip, 'rb') as f:
                self.copyfile(f, self.wfile)
            os.remove(tmpzip)
        elif os.path.isfile(path):
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", self.guess_type(self.path))
            self.send_header("Content-Length", os_stat(path).st_size)
            if inline:
                self.mime_header()
            else:
                self.send_header("Content-Disposition", 'attachment')
            self.end_headers()
            with open(path, 'rb') as f:
                self.copyfile(f, self.wfile)
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")

    def do_checkauth(self, path, url_token):
        """check authentication"""
        token = os.environ.get("PYWEBFS_TOKEN")
        if token and self.get_cookie("token") != token:
            if url_token != token:
                self.send_error(HTTPStatus.UNAUTHORIZED, "Invalid token")
                return False
            else:
                self.send_response(302)
                self.set_cookie('token', token)
                self.send_header('Location', path)
                self.end_headers()
                return False
                
        if self.path != '/login':
            if self.is_authenticated():
                return True
            else:
                if RE_AGENT.search(self.headers.get('User-Agent', '')):
                    self.send_response(302)
                    self.send_header('Location', '/login')
                else:
                    self.send_response(401)
                    self.send_header('WWW-Authenticate', 'Basic realm="Acces restreint"')
                self.end_headers()
                return False
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.write_html(HTML.format(title=self.server.title, charset=ENC))
            self.write_html(LOGIN.format(title=self.server.title))
            return False

    def do_GET(self):
        """do http calls"""
        user_agent = self.headers.get("User-Agent") or ""
        self.log_message(user_agent)
        browser = user_agent.split()[-1]
        if not browser.startswith("Edg"):
            m = RE_AGENT.search(user_agent)
            if m:
                browser = m[0]
        self.log_message(
            "%s: %s http://%s%s",
            browser,
            self.command,
            self.headers["Host"],
            self.path
        )

        if self.path == "/favicon.ico":
            self.path = "/favicon.svg"
        if self.path == "/favicon.svg":
            return self.send_data(FOLDER)
        elif self.path == "/style.css":
            return self.send_data(CSS)
        elif self.path == "/pywebfs.js":
            return self.send_data(JAVASCRIPT)
        p = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(p.query)
        token = q.get("token", [""])[0]
        search = q.get("search", [""])[0]
        searchtxt = q.get("searchtxt", [""])[0]
        download = q.get("download", [""])[0]
        noperm = q.get("noperm", [""])[0]
        if not self.do_checkauth(p.path, token):
            return

        global NO_PERM
        if noperm == "1":
            NO_PERM = True
        elif noperm == "0":
            NO_PERM = False
        path = fs_path(p.path)
        if download:
            return self.download("."+path)
        if not os.path.isdir("."+path):
            return self.download("."+path, inline=True)
        title = f"{self.server.title} - {html.escape(path, quote=False)}"
        htmldoc = [HTML.format(title=title, charset=ENC)]
        htmldoc.append('<body>')

        href = ['<a href="/" class="home" title="Home">&nbsp;</a>']
        fpath = "/"
        for dir in path.rstrip("/").split("/")[1:]:
            fpath += dir + "/"
            href.append('<a href="%s" class="path">/%s</a>' % (
                urllib.parse.quote(fpath, errors="surrogatepass"),
                html.escape(dir, quote=False),
            ))
        href.append('<a id=file class="path"></a>')
        header = [
            '<tr>\n<th colspan="100" class="header">',
            '  <div class="header">',
            '    <form name="search">',
            '      <input type="text" name="search" id="search" autocomplete="off">',
            '      <button type="submit" class="search" title="Search filenames in folder and subfolders"></button>',
        ]
        if not NO_SEARCH_TXT:
            header.append(
                '      <button type="submit" name="searchtxt" value=1 class="searchtxt" title="Search in text files"></button>'
            )
        header += [
            f'    {"".join(href)}',
            '    </form>',
            '  </div>',
            '</th>\n</tr>\n',
        ]
        self.header = "\n".join(header)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.write_html("\n".join(htmldoc))

        if p.query:
            if searchtxt:
                self.search_files(search, "." + path)
            elif search:
                self.find_files(search, "." + path)
            else:
                self.list_directory("." + path)
        else:
            self.list_directory("." + path)
        #self.write_html(enddoc)
        #self.write_html(JAVASCRIPT)
        self.write_html('<script type="text/javascript" src="/pywebfs.js"></script>\n')
        self.write_html('</body>\n</html>\n')

    def devnull(self):
        """unsupported method"""
        self.send_error(HTTPStatus.BAD_REQUEST, "Unsupported method")
        self.end_headers()
        return
    
    def do_POST(self):
        """get login post data"""
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = params.get('username', [None])[0]
            password = params.get('password', [None])[0]

            if username == self.server.userp[0] and self.server.userp[1] == password:
                self.send_response(302)
                self.set_cookie('session', self.server.uuid)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                sleep(2)
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()

    def get_cookie(self, cookie_name):
        """get cookie from request"""
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            cookie = SimpleCookie(cookie_header)
            cookie_val = cookie.get(cookie_name)
            if cookie_val:
                return cookie_val.value
        return None
    
    def set_cookie(self, cookie_name, value, max_age=None):
        """set cookie in response"""
        cookie = SimpleCookie()
        cookie[cookie_name] = value
        cookie[cookie_name]['path'] = '/'
        cookie[cookie_name]['httponly'] = True
        cookie[cookie_name]['samesite'] = 'Strict'
        if max_age:
            cookie[cookie_name]['max-age'] = max_age
        self.send_header('Set-Cookie', cookie.output(header=''))

    def is_authenticated(self):
        """check if user is authenticated"""
        if self.server.userp[0] is None:
            return True
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('Basic '):
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':')

            if username == self.server.userp[0] and self.server.userp[1] == password:
                return True
            else:
                sleep(2)

        session = self.get_cookie('session')
        if session and session == self.server.uuid:
            return True
        return False

    do_PUT    = devnull
    do_DELETE = devnull


class HTTPFileServer(ThreadingHTTPServer):
    """HTTPServer with httpfile"""

    def __init__(self, title, certfiles, userp, *args, **kwargs):
        """add title property"""
        self.title = title
        self.uuid = str(uuid4())
        self._auth = None
        self.userp = userp
        if userp[0]:
            self._auth = base64.b64encode(f"{userp[0]}:{userp[1]}".encode()).decode()

        super().__init__(*args, **kwargs)
        if certfiles[0]:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=certfiles[0], keyfile=certfiles[1])
            self.socket = context.wrap_socket(self.socket, server_side=True)
            # self.socket = ssl.wrap_socket (
            #     self.socket, 
            #     certfile=certfiles[0],
            #     keyfile=certfiles[1], 
            #     server_side=True
            # )

    def handle_error(self, request, client_address):
        return


def log_message(*args):
    """log message"""
    print(datetime.now().strftime("- - - [%d/%b/%Y %H:%M:%S]"), *args, file=sys.stderr)

def daemon_d(action, pidfilepath, hostname=None, args=None):
    """start/stop daemon"""
    import signal
    import daemon, daemon.pidfile

    pidfile = daemon.pidfile.TimeoutPIDLockFile(pidfilepath+".pid", acquire_timeout=30)
    if action == "stop":
        if pidfile.is_locked():
            pid = pidfile.read_pid()
            print(f"Stopping server pid {pid}")
            try:
                os.kill(pid, signal.SIGINT)
            except:
                return False
            return True
    elif action == "status":
        status = pidfile.is_locked()
        if status:
            print(f"pywebfs running pid {pidfile.read_pid()}")
            return True
        print("pywebfs not running")
        return False
    elif action == "start":
        print(f"Starting server")
        log = open(pidfilepath + ".log", "ab+")
        daemon_context = daemon.DaemonContext(
            stderr=log,
            pidfile=pidfile,
            umask=0o077,
            working_directory=args.dir,
        )
        with daemon_context:
            log_message("Starting server")
            with init_server(hostname, args) as server:
                try:
                    server.serve_forever()
                except KeyboardInterrupt:
                    log_message("Stopping server")


def init_server(hostname, args, token=None):
    """initialize http server"""
    prefix = "https" if args.cert else "http"
    suffix = f"?token={token}" if token else ""
    log_message(f"Starting {prefix} server listening on {args.listen} port {args.port}")
    log_message(f"{prefix} server : {prefix}://{hostname}:{args.port}{suffix}")
    try:
        return HTTPFileServer(
            args.title, 
            (args.cert, args.key),
            (args.user, args.password),
            (args.listen, args.port), HTTPFileHandler)
    except OSError as e:
        print(e)
        sys.exit(1)


def main():
    """start http server according to args"""
    global NO_SEARCH_TXT, NO_PERM, HIDDEN

    parser = argparse.ArgumentParser(prog="pywebfs")
    parser.add_argument(
        "-l", "--listen", type=str, default="0.0.0.0", help="HTTP server listen address"
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
        help="Web html title",
    )
    parser.add_argument("-c", "--cert", type=str, help="Path to https certificate")
    parser.add_argument("-k", "--key", type=str, help="Path to https certificate key")
    parser.add_argument("-u", "--user", type=str, help="username")
    parser.add_argument("-P", "--password", type=str, help="password")
    parser.add_argument("-s", "--start", action="store_true", help="Start as a daemon")
    parser.add_argument("-g", "--gencert", action="store_true", help="https server self signed cert")
    parser.add_argument("--nosearch", action="store_true", help="No search in text files button")
    parser.add_argument("--noperm", action="store_true", help="No display permissions and owner/group")
    parser.add_argument("-H", "--hidden", nargs="+", help="file/folder patterns to hide")
    parser.add_argument("-T", "--tokenurl", action="store_true", help="use url token for authentication")
    parser.add_argument("action", nargs="?", help="daemon action start/stop/restart/status", choices=["start","stop","restart","status"])
    
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
    NO_SEARCH_TXT = args.nosearch
    if args.hidden:
        HIDDEN = args.hidden
    if args.noperm:
        NO_PERM = True
    hostname = resolve_hostname(gethostname())
    if not os.path.exists(PYWFSDIR):
        os.mkdir(PYWFSDIR, mode=0o700)

    if args.gencert:
        args.cert = args.cert or f"{PYWFSDIR}/{hostname}.crt"
        args.key = args.key or f"{PYWFSDIR}/{hostname}.key"
        if not os.path.exists(args.cert):
            (cert, key) = generate_selfsigned_cert(hostname)
            with open(args.cert, "wb") as fd:
                fd.write(cert)
            with open(args.key, "wb") as fd:
                fd.write(key)
    if args.user and not args.password:
        args.password = secrets.token_urlsafe(13)
        print(f"Generated password: {args.password}")
    if args.tokenurl:
        token = os.environ.get("PYWEBFS_TOKEN", token_urlsafe())
        os.environ["PYWEBFS_TOKEN"] = token
    else:
        token = None
    pidfile = f"{PYWFSDIR}/pwfs_{args.listen}:{args.port}"

    if args.action == "restart":
        daemon_d("stop", pidfile)
        args.action = "start"
    if args.action:
        sys.exit(not daemon_d(args.action, pidfile, hostname, args))
    else:
        with init_server(hostname, args, token) as server:
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                log_message("Stopping server")
                server.socket.close()


if __name__ == "__main__":
    main()
