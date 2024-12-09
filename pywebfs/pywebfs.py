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
from http import HTTPStatus
import ssl
import urllib.parse
from datetime import datetime, timedelta, timezone
import ipaddress
import secrets

NO_SEARCH_TXT = False

FOLDER = '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path id="SVGCleanerId_0" style="fill:#FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path> <g> <path id="SVGCleanerId_0_1_" style="fill:#FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path> </g> <path style="fill:#EFF2FA;" d="M485.517,70.621H26.483c-4.875,0-8.828,3.953-8.828,8.828v44.138h476.69V79.448 C494.345,74.573,490.392,70.621,485.517,70.621z"></path> <rect x="17.655" y="105.931" style="fill:#E1E6F2;" width="476.69" height="17.655"></rect> <path style="fill:#FFD782;" d="M494.345,88.276H217.318c-3.343,0-6.4,1.889-7.895,4.879l-10.336,20.671 c-2.99,5.982-9.105,9.76-15.791,9.76H55.05c-6.687,0-12.801-3.778-15.791-9.76L28.922,93.155c-1.495-2.99-4.552-4.879-7.895-4.879 h-3.372C7.904,88.276,0,96.18,0,105.931v335.448c0,9.751,7.904,17.655,17.655,17.655h476.69c9.751,0,17.655-7.904,17.655-17.655 V105.931C512,96.18,504.096,88.276,494.345,88.276z"></path> <path style="fill:#FFC36E;" d="M485.517,441.379H26.483c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h459.034c4.875,0,8.828,3.953,8.828,8.828l0,0C494.345,437.427,490.392,441.379,485.517,441.379z"></path> <path style="fill:#EFF2FA;" d="M326.621,220.69h132.414c4.875,0,8.828-3.953,8.828-8.828v-70.621c0-4.875-3.953-8.828-8.828-8.828 H326.621c-4.875,0-8.828,3.953-8.828,8.828v70.621C317.793,216.737,321.746,220.69,326.621,220.69z"></path> <path style="fill:#C7CFE2;" d="M441.379,167.724h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,163.772,446.254,167.724,441.379,167.724z"></path> <path style="fill:#D7DEED;" d="M441.379,203.034h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,199.082,446.254,203.034,441.379,203.034z"></path> </g></svg>'
FOLDER_CSS = '<svg width="16px" height="16px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="%23000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path id="SVGCleanerId_0" style="fill:%23FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path><g><path id="SVGCleanerId_0_1_" style="fill:%23FFC36E;" d="M183.295,123.586H55.05c-6.687,0-12.801-3.778-15.791-9.76l-12.776-25.55 l12.776-25.55c2.99-5.982,9.103-9.76,15.791-9.76h128.246c6.687,0,12.801,3.778,15.791,9.76l12.775,25.55l-12.776,25.55 C196.096,119.808,189.983,123.586,183.295,123.586z"></path></g><path style="fill:%23EFF2FA;" d="M485.517,70.621H26.483c-4.875,0-8.828,3.953-8.828,8.828v44.138h476.69V79.448 C494.345,74.573,490.392,70.621,485.517,70.621z"></path><rect x="17.655" y="105.931" style="fill:%23E1E6F2;" width="476.69" height="17.655"></rect><path style="fill:%23FFD782;" d="M494.345,88.276H217.318c-3.343,0-6.4,1.889-7.895,4.879l-10.336,20.671 c-2.99,5.982-9.105,9.76-15.791,9.76H55.05c-6.687,0-12.801-3.778-15.791-9.76L28.922,93.155c-1.495-2.99-4.552-4.879-7.895-4.879 h-3.372C7.904,88.276,0,96.18,0,105.931v335.448c0,9.751,7.904,17.655,17.655,17.655h476.69c9.751,0,17.655-7.904,17.655-17.655 V105.931C512,96.18,504.096,88.276,494.345,88.276z"></path><path style="fill:%23FFC36E;" d="M485.517,441.379H26.483c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h459.034c4.875,0,8.828,3.953,8.828,8.828l0,0C494.345,437.427,490.392,441.379,485.517,441.379z"></path><path style="fill:%23EFF2FA;" d="M326.621,220.69h132.414c4.875,0,8.828-3.953,8.828-8.828v-70.621c0-4.875-3.953-8.828-8.828-8.828 H326.621c-4.875,0-8.828,3.953-8.828,8.828v70.621C317.793,216.737,321.746,220.69,326.621,220.69z"></path><path style="fill:%23C7CFE2;" d="M441.379,167.724h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,163.772,446.254,167.724,441.379,167.724z"></path><path style="fill:%23D7DEED;" d="M441.379,203.034h-97.103c-4.875,0-8.828-3.953-8.828-8.828l0,0c0-4.875,3.953-8.828,8.828-8.828 h97.103c4.875,0,8.828,3.953,8.828,8.828l0,0C450.207,199.082,446.254,203.034,441.379,203.034z"></path></g></svg>'
UPFOLDER_CSS = '<svg width="16px" height="16px" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M12.9998 8L6 14L12.9998 21" stroke="%23000000" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"></path><path d="M6 14H28.9938C35.8768 14 41.7221 19.6204 41.9904 26.5C42.2739 33.7696 36.2671 40 28.9938 40H11.9984" stroke="%23000000" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"></path></g></svg>'
HOME_CSS = '<svg width="16px" height="16px" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M1 6V15H6V11C6 9.89543 6.89543 9 8 9C9.10457 9 10 9.89543 10 11V15H15V6L8 0L1 6Z" fill="%23000000"></path></g></svg>'
FILE_CSS = '<svg width="16px" height="16px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="%23000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M6 10h12v1H6zM3 1h12.29L21 6.709V23H3zm12 6h5v-.2L15.2 2H15zM4 22h16V8h-6V2H4zm2-7h12v-1H6zm0 4h9v-1H6z"></path><path fill="none" d="M0 0h24v24H0z"></path></g></svg>'
LINK_CSS = '<svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M9.16488 17.6505C8.92513 17.8743 8.73958 18.0241 8.54996 18.1336C7.62175 18.6695 6.47816 18.6695 5.54996 18.1336C5.20791 17.9361 4.87912 17.6073 4.22153 16.9498C3.56394 16.2922 3.23514 15.9634 3.03767 15.6213C2.50177 14.6931 2.50177 13.5495 3.03767 12.6213C3.23514 12.2793 3.56394 11.9505 4.22153 11.2929L7.04996 8.46448C7.70755 7.80689 8.03634 7.47809 8.37838 7.28062C9.30659 6.74472 10.4502 6.74472 11.3784 7.28061C11.7204 7.47809 12.0492 7.80689 12.7068 8.46448C13.3644 9.12207 13.6932 9.45086 13.8907 9.7929C14.4266 10.7211 14.4266 11.8647 13.8907 12.7929C13.7812 12.9825 13.6314 13.1681 13.4075 13.4078M10.5919 10.5922C10.368 10.8319 10.2182 11.0175 10.1087 11.2071C9.57284 12.1353 9.57284 13.2789 10.1087 14.2071C10.3062 14.5492 10.635 14.878 11.2926 15.5355C11.9502 16.1931 12.279 16.5219 12.621 16.7194C13.5492 17.2553 14.6928 17.2553 15.621 16.7194C15.9631 16.5219 16.2919 16.1931 16.9495 15.5355L19.7779 12.7071C20.4355 12.0495 20.7643 11.7207 20.9617 11.3787C21.4976 10.4505 21.4976 9.30689 20.9617 8.37869C20.7643 8.03665 20.4355 7.70785 19.7779 7.05026C19.1203 6.39267 18.7915 6.06388 18.4495 5.8664C17.5212 5.3305 16.3777 5.3305 15.4495 5.8664C15.2598 5.97588 15.0743 6.12571 14.8345 6.34955" stroke="%23000000" stroke-width="2" stroke-linecap="round"></path></g></svg>'
SEARCH_CSS = '<svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M16.6725 16.6412L21 21M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="%23000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></g></svg>'
SEARCH_TXT_CSS = '<svg width="16px" height="16px" viewBox="6 5 14 14" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path fill-rule="evenodd" clip-rule="evenodd" d="M11.132 9.71395C10.139 11.2496 10.3328 13.2665 11.6 14.585C12.8468 15.885 14.8527 16.0883 16.335 15.065C16.6466 14.8505 16.9244 14.5906 17.159 14.294C17.3897 14.0023 17.5773 13.679 17.716 13.334C18.0006 12.6253 18.0742 11.8495 17.928 11.1C17.7841 10.3573 17.4268 9.67277 16.9 9.12995C16.3811 8.59347 15.7128 8.22552 14.982 8.07395C14.2541 7.92522 13.4982 8.00197 12.815 8.29395C12.1254 8.58951 11.5394 9.08388 11.132 9.71395Z" stroke="%23000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M17.5986 13.6868C17.2639 13.4428 16.7947 13.5165 16.5508 13.8513C16.3069 14.1861 16.3806 14.6552 16.7154 14.8991L17.5986 13.6868ZM19.0584 16.6061C19.3931 16.85 19.8623 16.7764 20.1062 16.4416C20.3501 16.1068 20.2764 15.6377 19.9416 15.3938L19.0584 16.6061ZM7.5 12.7499C7.91421 12.7499 8.25 12.4142 8.25 11.9999C8.25 11.5857 7.91421 11.2499 7.5 11.2499V12.7499ZM5.5 11.2499C5.08579 11.2499 4.75 11.5857 4.75 11.9999C4.75 12.4142 5.08579 12.7499 5.5 12.7499V11.2499ZM7.5 15.7499C7.91421 15.7499 8.25 15.4142 8.25 14.9999C8.25 14.5857 7.91421 14.2499 7.5 14.2499V15.7499ZM5.5 14.2499C5.08579 14.2499 4.75 14.5857 4.75 14.9999C4.75 15.4142 5.08579 15.7499 5.5 15.7499V14.2499ZM8.5 9.74994C8.91421 9.74994 9.25 9.41415 9.25 8.99994C9.25 8.58573 8.91421 8.24994 8.5 8.24994V9.74994ZM5.5 8.24994C5.08579 8.24994 4.75 8.58573 4.75 8.99994C4.75 9.41415 5.08579 9.74994 5.5 9.74994V8.24994ZM16.7154 14.8991L19.0584 16.6061L19.9416 15.3938L17.5986 13.6868L16.7154 14.8991ZM7.5 11.2499H5.5V12.7499H7.5V11.2499ZM7.5 14.2499H5.5V15.7499H7.5V14.2499ZM8.5 8.24994H5.5V9.74994H8.5V8.24994Z" fill="%23000000"></path></g></svg>'
SEARCH_TXT_CSS = '<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" fill="%23000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><g id="Layer_2" data-name="Layer 2"><g id="Icons"><g><rect width="48" height="48" fill="none"></rect><path d="M29,27H13a2,2,0,0,1,0-4H29a2,2,0,0,1,0,4ZM13,31a2,2,0,0,0,0,4h8a2,2,0,0,0,0-4Zm24-5a2,2,0,0,0-2,2V42H7V8H17a2,2,0,0,0,0-4H5A2,2,0,0,0,3,6V44a2,2,0,0,0,2,2H37a2,2,0,0,0,2-2V28A2,2,0,0,0,37,26Zm7.4-.6a1.9,1.9,0,0,1-2.8,0l-5.1-5.1h0A10.4,10.4,0,0,1,31,22a10.1,10.1,0,0,1-7.1-3H13a2,2,0,0,1,0-4h8.5a9.9,9.9,0,0,1-.5-3,10,10,0,0,1,20,0,10.4,10.4,0,0,1-1.6,5.5h-.1l5.1,5.1A1.9,1.9,0,0,1,44.4,25.4ZM27.5,15a.9.9,0,0,1,1-1h4V13h-3a2,2,0,0,1-2-2V10a2,2,0,0,1,2-2H30V6.1a6,6,0,0,0,0,11.8V16H28.5A.9.9,0,0,1,27.5,15ZM37,12a6,6,0,0,0-5-5.9V8h1.5a.9.9,0,0,1,1,1,.9.9,0,0,1-1,1h-4v1h3a2,2,0,0,1,2,2v1a2,2,0,0,1-2,2H32v1.9l1.6-.5.6-.3a.1.1,0,0,1,.1-.1l.7-.5a.1.1,0,0,1,.1-.1l.6-.6h0l.5-.8h0l.2-.4A5.5,5.5,0,0,0,37,12Z"></path></g></g></g></g></svg>'
CSS = f"""
    html, body: {{
        margin:0px;
        border:0px;
    }}
    body {{
        padding: 0px;
        background-color: #333;
        font-family: -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;;
        font-size: 1em;
    }}
    div {{
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
    }}
    pre {{
        margin: 0;
        line-height: 105%
    }}
    tr:nth-of-type(even) {{
        background-color: #e3e3f3;
    }}
    tr:hover {{
        background-color: #ccf;
    }}
    th {{
        text-align: left;
        font-weight: unset;
        color: #5c5c5c;
    }}
    td, th {{
        vertical-align: top;
        padding-right: 20px;
        white-space: nowrap;
    }}
    th.size {{
        text-align: center;
    }}
    /* size num */
    #files tr td:nth-child(2) {{
        font-variant-numeric: tabular-nums;
        padding-right: 5px;
        text-align: right;
    }}
    /* date */
    #files tr td:nth-child(4) {{
        font-variant-numeric: tabular-nums;    
    }}

    .header {{
        background-color: #aaa;
        z-index: 2;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px 10px 10px;
        display: flex;
        line-height: 120%;
    }}
    .mask {{
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
    .list {{
        width: calc(100% - 20px);
        margin: 0px 0px 10px 0px;
        background-color: #F3F4FF;
        border-radius: 0px 10px 10px 10px;
        z-index: 3;
        display: table;
    }}
    a {{ text-decoration: none; }}
    ul {{ 
        line-height: 150%;
        list-style-type: none;
        padding: 10px 20px;
        margin: 0;
    }}
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
    .search {{
        background: url('data:image/svg+xml;utf8,{SEARCH_CSS}') no-repeat;
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
        cursor:pointer;
    }}
    .path {{
        vertical-align: middle;
        color: #000;
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
    .folder, .file, .link, .upfolder {{
        display: inline-block;
        text-indent: 20px;
        background-size: 16px 16px;
        background-position-y: 4px;
    }}
    table {{
        border-spacing: 0;
    }}
    .found {{
        background: #bfc;
    }}
    #info {{
        visibility: hidden;
        position: absolute;
    }}
    th.name {{
        min-width: 400px;
    }}
    div.name {{
        float: left;
    }}
    .info {{
        float: right;
        font-size: 0.8em;
    }}
    @media screen and (max-device-width: 480px){{
        body {{
            -webkit-text-size-adjust: 180%;
        }}
        .search, .home, .folder, .file, .link, .upfolder {{
            background-size: 32px 32px;
            text-indent: 40px;
        }}
    }}

"""

ENC = sys.getfilesystemencoding()
HTML = f"""
<!DOCTYPE HTML>
<html lang="en">
<head>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<meta charset="{ENC}">
"""
#<link rel="stylesheet" href="/style.css">
# <style>
# {CSS}
# </style>

RE_AGENT = re.compile(r"(Edg|Chrome|Safari|Firefox|Opera|Lynx)[^ ]*")

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
    try:
        return urllib.parse.unquote(path, errors="surrogatepass")
    except UnicodeDecodeError:
        return urllib.parse.unquote(path)

def convert_size(size_bytes):
    if size_bytes == 0:
        return ("0","B")

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    double_size = float(size_bytes)
    while double_size >= 1000 and i < len(size_name) - 1:
        double_size /= 1000.0
        i += 1

    return (str(round(double_size,1)), size_name[i])


def is_binary_file(path):
    if not os.path.isfile(path):
        return None
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    with open(path, "rb") as fd:
        bytes = fd.read(1024)
    return bool(bytes.translate(None, textchars))

def grep(rex, path, first=False):
    if is_binary_file(path):
        return []
    founds = []
    with open(path, "r") as fd:
        try:
            for line in fd:
                line = line.rstrip("\r\n").rstrip("\n")
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
        except:
            pass
    return founds

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


class HTTPFileHandler(SimpleHTTPRequestHandler):
    """Class handler for HTTP"""

    def _set_response(self, status_code, data):
        """build response"""

        self.send_response(status_code)
        encoded = data.encode(ENC, "surrogateescape")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        try: 
            self.wfile.write(encoded)
        except:
            pass

    def finish(self):
        try:
            return super().finish()
        except ConnectionResetError:
            pass

    def end_headers(self):
        p = urllib.parse.urlparse(self.path)
        fpath = fs_path("." + p.path)
        is_html = p.query or os.path.isdir(fpath)
        # adds extra headers to download/display file types.
        if is_html:
            self.send_header("Content-Type", f"text/html; charset={ENC}")
        else:
            mimetype = self.guess_type(self.path)
            if mimetype == "application/octet-stream" and is_binary_file(fpath) == False:
                mimetype = "text/plain"
            self.log_message(mimetype)
            if mimetype in ["text/plain"]:
                self.send_header("Content-Disposition", "inline")
            self.send_header("Content-Type", mimetype)
            if self.path in ["/style.css", "/favicon.ico"]:
                self.send_header("Cache-Control", "max-age=604800")
            else:
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
        super().end_headers()


    def find_files(self, search, path):
        """ find files recursively with name contains any word in search"""
        rexp = []
        for s in search.split():
            try:
                rexp.append(re.compile(accent_re(s), re.IGNORECASE))
            except:
                rexp.append(re.compile(accent_re(re.escape(s))))
        self.write_html('<table id="files">\n<tr><th class="name"><div class="name">Name</div><div class="info" id="nameinfo"></div></th><th class="size" colspan=2>Size</th><th>Modified</th><th style=width:100%></th></tr>')
        nbfiles = 0
        size = 0
        self.log_message(path)
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if all([bool(x.search(filename)) for x in rexp]):
                    fpath = os.path.join(dirpath, filename)
                    stat = os.stat(fpath)
                    nbfiles += 1
                    size += stat.st_size
                    size_unit = convert_size(stat.st_size)
                    self.write_html(
                        '<tr><td><li><a href="%s" class="file">%s</a></li></td><td>%s</td><td>%s</td><td>%s</td><td></td></tr>'
                        % (
                            urllib.parse.quote(fpath[1:].replace("\\", "/"), errors="surrogatepass"),
                            html.escape(filename, quote=False),
                            size_unit[0], size_unit[1],
                            datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        )
                    )
        self.write_html("</table>")
        s = "s" if nbfiles>1 else ""            
        self.write_html(f'<p id="info">{nbfiles} file{s} - {" ".join(convert_size(size))}</p>')

    def search_files(self, search, path):
        """ find files recursively containing search pattern"""
        
        try:
            rex = re.compile(accent_re(search), re.IGNORECASE)
        except:
            rex = re.compile(accent_re(re.escape(search)), re.IGNORECASE)
        self.write_html('<table class="searchresult">\n<th class="name"><div class="name">Name</div><div class="info" id="nameinfo"></div></th><th>Text</th><th style=width:100%></th></tr>')
        nbfiles = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                fpath = os.path.join(dirpath, filename)
                found = grep(rex, fpath, first=False)
                if found:
                    nbfiles += 1
                    fpath = fpath.replace("\\", "/")[1:]
                    urlpath = urllib.parse.quote(fpath, errors="surrogatepass")
                    self.write_html('''
                        <tr>
                            <td><li><a href="%s" class="file" title="%s">%s</a></li></td>
                            <td><pre>%s</pre></td>
                            <td></td>
                        </tr>
                        '''
                        % (
                            urlpath,
                            urlpath,
                            html.escape(filename, quote=False),
                            "\n".join(found)
                        )
                    )
        self.write_html('</table>')
        s = "s" if nbfiles>1 else ""
        self.write_html(f'<p id="info">{nbfiles} file{s}</p>')
    
    def write_html(self, data):
        encoded = data.encode(ENC, "surrogateescape")
        try: 
            self.wfile.write(encoded)
        except:
            pass


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
            return ""
        self.write_html('<table id="files">\n<thead><tr><th class="name"><div class="name">Name</div><div class="info" id="nameinfo"></div></th><th class="size" colspan=2>Size</th><th>Modified</th><th style=width:100%></th></tr></thead><tbody>')
        if path != "./":
            parentdir = os.path.dirname(path[1:].rstrip("/"))
            stat = os.stat("."+parentdir)
            if parentdir != "/":
                parentdir += "/"
            size_unit = convert_size(stat.st_size)
            self.write_html(
                '<tr><td><li><a href="%s" class="upfolder">..</a></li></td><td>%s</td><td>%s</td><td>%s</td><td></td></tr>'
                % (
                    urllib.parse.quote(parentdir , errors='surrogatepass'),
                    size_unit[0], size_unit[1],
                    datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                )
            )
        list.sort(key=lambda a: a.lower())
        nbfiles = 0
        size = 0
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            stat = os.stat(fullname)
            if os.path.islink(fullname):
                img = "link"
                linkname = name + "/"
            elif os.path.isdir(fullname):
                linkname = name + "/"
                img = "folder"
            else:
                img = "file"
                nbfiles += 1
                size += stat.st_size
            size_unit = convert_size(stat.st_size)
            self.write_html(
                '<tr><td><li><a href="%s" class="%s">%s</a></li></td><td>%s</td><td>%s</td><td>%s</td><td></td></tr>'
                % (
                    urllib.parse.quote(linkname, errors="surrogatepass"),
                    img,
                    html.escape(displayname, quote=False),
                    size_unit[0], size_unit[1],
                    datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                )
            )
        self.write_html("</tbody></table>")
        s = "s" if nbfiles>1 else ""
        self.write_html(f'<p id="info">{nbfiles} file{s} - {" ".join(convert_size(size))}</p>')

    def do_HEAD(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(HTTPStatus.UNAUTHORIZED)
        self.send_header("WWW-Authenticate", 'Basic realm="Test"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """do http calls"""
        user_agent = self.headers.get("User-Agent") or ""
        #self.log_message(user_agent)
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
        if self.server._auth:
            if self.headers.get("Authorization") == None:
                self.do_AUTHHEAD()
                self.wfile.write(b"no auth header received")
                return
            elif self.headers.get("Authorization") != "Basic " + self.server._auth:
                self.do_AUTHHEAD()
                self.wfile.write(self.headers.get("Authorization").encode())
                self.wfile.write(b"not authenticated")
                return

        if self.path == "/favicon.ico":
            self.path = "/favicon.svg"
        if self.path == "/favicon.svg":
            return self._set_response(HTTPStatus.OK, FOLDER)
        elif self.path == "/style.css":
            return self._set_response(HTTPStatus.OK, CSS)
        p = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(p.query)
        search = q.get("search", [""])[0]
        searchtxt = q.get("searchtxt", [""])[0]
        path = displaypath = fs_path(p.path)
        displaypath = html.escape(displaypath, quote=False)
        if not os.path.isdir("."+path):
            return super().do_GET()

        title = f"{self.server.title} - {displaypath}"
        htmldoc = HTML
        htmldoc += f"<title>{title}</title>\n</head>"
        htmldoc += "<body>"

        href = '<a href="/" class="home" title="Home">/</a>'
        fpath = "/"
        for dir in path.rstrip("/").split("/")[1:]:
            fpath += dir + "/"
            href += '<a href="%s" class="path">%s/</a>' % (
                urllib.parse.quote(fpath, errors="surrogatepass"),
                html.escape(dir, quote=False),
            )
        htmldoc += '<div class=mask>'
        htmldoc += '<div class=header>'
        htmldoc += "<form name=search>"
        htmldoc += f"<input type=text name=search value='{search}' autofocus>"
        htmldoc += '<button type=submit class="search" title="Search filenames">&nbsp;&nbsp;&nbsp;</button>'
        if not NO_SEARCH_TXT:
            htmldoc += '<button type=submit name="searchtxt" value=1 class="searchtxt" title="Search in text files">&nbsp;&nbsp;&nbsp;</button>'
        htmldoc += f"{href}\n</form>"
        htmldoc += "</div></div>"
        htmldoc += "<div class=list><ul>"

        enddoc = "\n</ul>\n</div>"

        self.send_response(HTTPStatus.OK)
        self.end_headers()

        self.write_html(htmldoc)

        if p.query:
            if searchtxt:
                self.search_files(search, "." + path)
            else:
                self.find_files(search, "." + path)
        else:
            self.list_directory("." + path)
        self.write_html(enddoc)
        self.write_html('<script>document.getElementById("nameinfo").innerHTML=document.getElementById("info").innerHTML;</script>')
        self.write_html('</body>\n</html>\n')

    def devnull(self):
        self.send_error(HTTPStatus.BAD_REQUEST, "Unsupported method")
        super().end_headers()
        return
    
    do_POST   = devnull
    do_PUT    = devnull
    do_DELETE = devnull



class HTTPFileServer(ThreadingHTTPServer):
    """HTTPServer with httpfile"""

    def __init__(self, title, certfiles, userp, *args, **kwargs):
        """add title property"""
        self.title = title
        self._auth = None
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

def main():
    """start http server according to args"""
    global NO_SEARCH_TXT

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
    parser.add_argument("-c", "--cert", type=str, help="Path to https certificate")
    parser.add_argument("-k", "--key", type=str, help="Path to https certificate key")
    parser.add_argument("-u", "--user", type=str, help="username")
    parser.add_argument("-P", "--password", type=str, help="password")
    parser.add_argument("-D", "--daemon", action="store_true", help="Start as a daemon")
    parser.add_argument("-g", "--gencert", type=str, nargs="+", help="hostname ipaddr  https server self signed cert")
    parser.add_argument("-n", "--nosearch", action="store_true", help="No search in text files button")
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
    if args.gencert:
        hostname = args.gencert.pop(0)
        ips = args.gencert
        certdir = os.path.expanduser("~/.pywebfs")
        if not os.path.exists(certdir):
            os.mkdir(certdir, mode=0o700)
        args.cert = args.cert or f"{certdir}/{hostname}.crt"
        args.key = args.key or f"{certdir}/{hostname}.key"
        if not os.path.exists(args.cert):
            (cert, key) = generate_selfsigned_cert(hostname, ips, None)
            with open(args.cert, "wb") as fd:
                fd.write(cert)
            with open(args.key, "wb") as fd:
                fd.write(key)
    prefix = "https" if args.cert else "http"
    print(f"Starting {prefix} server : {prefix}://{args.server}:{args.port}")
    if args.user and not args.password:
        args.password = secrets.token_urlsafe(13)
        print(f"Generated password: {args.password}")
    server = HTTPFileServer(
        args.title, 
        (args.cert, args.key),
        (args.user, args.password),
        (args.server, args.port), HTTPFileHandler)

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
            print(f"Stopping {prefix} server")
            sys.exit(0)


if __name__ == "__main__":
    main()
