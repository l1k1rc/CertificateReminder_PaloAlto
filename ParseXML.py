#!/usr/bin/env python3

import xml
from datetime import datetime
from xml.dom import minidom

from Firewall import Firewall

__author__ = "SAINT-AMAND Matthieu"
__copyright__ = "Copyright 2007, The Cogent Project"
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "SAINT-AMAND Matthieu"
__email__ = "matthieu.saint-amand@sagemcom.com"
__status__ = "Proof of Concept"

HEADER = u"""
           <head>
             <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
             <title>html title</title>
             <style type="text/css" media="screen">
                span{
                    border-color:  #979797;
                    margin:.2em .5em;
                    padding:0.1em .5em; 
                    border:2px inset #0080FF;
                    font-family: 'Courier', serif;
                    color:black;
                }
                h2{
                    color: #3f3f3f;
                    font-size: 45px;
                    font-family: 'Courier', serif;
                    font-weight: normal;
                    line-height: 48px;
                    margin: 0;
                    margin-bottom:10px;
                }
                p{
                    font-family: 'Courier', serif;
                }
               /* Table Styles */
               .fl-table {
                   margin: 10px;
                   padding: 10px;
                   border-color: #aaaaaa;
                   border-radius: 5px;
                   border-style: dotted;
                   border-width: 3px;
                   font-size: 14px;
                   font-weight: normal;
                   border-collapse: collapse;
                   width: 100%;
                   max-width: 100%;
                   white-space: nowrap;
                   background-color: white;
               }
               .fl-table td, .fl-table th {
                   text-align: center;
                   padding: 8px;
               }

               .fl-table thead th {
                   color: #ffffff;
                   background: #0080FF;
               }
           </style>
           </head>
           <body>
                   <h2>Certificate reminder</h2>
                   <b>&nbsp;<span>""" + datetime.now().strftime("%b %d, %H:%M %Y") + """</span></b>
                   <p>&nbsp;All the logs of the day of <b>02/07/2020</b>. Please find below the information concerning them. </p>
                   <div class="table-wrapper">
                       <table class="fl-table">
                <thead>
                <tr>
                       <th>Hostname</th>
                       <th>Certificate</th>
                       <th>Creation time</th>
                       <th>Expiration time</th>
                       <th>Certificate's validity</th>
                   </tr>
                </thead>
                <tbody>
        """

FOOTER = u"""
                <tbody>
            </table>
            </div>
        </body>
        """

"""
Function to find a particular node in an XML file.

:param document: document from xml.dom package 
:type document: xml.dom.minidom.parse()
:param field: node name
:type field: str
:param d_values: array filled after calling this function
:type d_values: array()
:returns: Procedural recursive function
:rtype: //

"""


def readConf(document, field, d_values):
    for child in document.childNodes:
        if child.nodeType == child.TEXT_NODE:
            if document.tagName == field:
                d_values.append(child.data)
        if child.nodeType == xml.dom.Node.ELEMENT_NODE:
            readConf(child, field, d_values)


def readSpecificChildAttr(document, parentTag, childTag, attrValue):
    itemList = document.getElementsByTagName(parentTag)  # certificate
    data = []
    for cert in itemList[0].getElementsByTagName(childTag):  # entry
        data.append(get_all_text(cert.attributes[attrValue]))  # entry
    return data

    # print(get_all_text(itemList[0].getElementsByTagName('entry')[0].attributes['name']))
    # for val in itemList:
    #    print("Entry name : ", val.getElementByTagName('entry').attributes['name'].value)
    # print("Len : ", itemList[].attributes['name'].value)


def get_all_text(node):
    if node.nodeType == node.TEXT_NODE:
        return node.data
    else:
        text_string = ""
        for child_node in node.childNodes:
            text_string += get_all_text(child_node)
        return text_string


def organizeData(XML_f, HTML_file):
    # Retrieve the XML file
    dom = xml.dom.minidom.parse(XML_f)
    # Result assignment
    compact_data = dict()
    # Assignment
    dexpire_values = []
    dexpire_epoch = []
    dcreated_values = []
    fw_hostname = []
    # Calls
    readConf(dom.documentElement, FW_NAME, fw_hostname)
    readConf(dom.documentElement, EXPIRE, dexpire_values)
    readConf(dom.documentElement, CREATED, dcreated_values)
    readConf(dom.documentElement, EXPIRY_EPOCH, dexpire_epoch)
    readSpecificChildAttr(dom, 'certificate', CERTIFICATE, 'name')
    # Positioning
    for i in range(len(dcreated_values)):
        compact_data[readSpecificChildAttr(dom, 'certificate', CERTIFICATE, 'name')[i]] = [dcreated_values[i],
                                                                                           dexpire_epoch[i]]
    fw = Firewall(fw_hostname.__getitem__(0), compact_data)
    fw.generateHTML(HTML_file)


if __name__ == '__main__':
    # Assignment
    d_actual = datetime.now().strftime("%b %d %H:%M:%S %Y")
    filename = 'data/PA-500_running-config.xml'
    fileTest = 'data/RMM_Ishtar_001801007801.xml'
    html_file = 'data/data_mail.html'
    # Constants
    CERTIFICATE = 'entry'
    FW_NAME = 'hostname'
    EXPIRE = 'not-valid-after'
    CREATED = 'not-valid-before'
    EXPIRY_EPOCH = 'expiry-epoch'
    # Calls
    HTML = open(html_file, "w")
    HTML.write('')
    HTML = open(html_file, "a")

    HTML.write(HEADER)
    organizeData(filename, HTML)
    organizeData(fileTest, HTML)
    HTML.write(FOOTER)
