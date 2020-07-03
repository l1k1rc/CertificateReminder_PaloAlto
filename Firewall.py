#!/usr/bin/env python3

import time
from datetime import datetime


class Firewall:
    def __init__(self, fw_name, fw_certificate):
        self.name = fw_name
        self.certificates = fw_certificate
        self.validity = bool
        self.mail = ''

    @staticmethod
    def sendMail():
        # TODO
        print()

    @staticmethod
    def convertStringToDate(strV):
        return datetime.strptime(str(strV).replace("GMT", "").strip(), "%b %d %H:%M:%S %Y")

    def isValid(self, this_date):
        # Retrieves the current data in "date" format
        d_actual = self.convertStringToDate(datetime.now().strftime("%b %d %H:%M:%S %Y"))

        # Stores strings corresponding to validation images
        notValid = "<img width=\"28\" src=\"cid:image3\">"
        valid = "<img width=\"28\" src=\"cid:image2\">"
        if self.convertStringToDate(time.strftime('%b %d %H:%M:%S %Y', time.localtime(int(this_date)))) <= d_actual:
            return notValid
        else:
            return valid

    def generateHTML(self, HTML_file):
        v_iterator = iter(self.certificates.values())
        print(next(v_iterator))
        for key in self.certificates:
            print(key, '->', self.certificates[key])
            html_str = "<tr>\n" \
                       "\t<th>" + str(self.name) + "</th>\n" \
                                                   "\t<th>" + key + "</th>\n" \
                                                                    "\t<th>" + self.certificates[key][0] + "</th>\n" \
                                                                                                           "\t<th>" + \
                       time.strftime('%b %d %H:%M:%S %Y', time.localtime(int(self.certificates[key][1]))) + "</th>\n" \
                                                                                                            "\t<th>" + self.isValid(
                self.certificates[key][1]) + "</th>\n" \
                                             "</tr>\n"
            self.mail = self.mail + html_str
        print(self.mail)
        HTML_file.write(self.mail)

    def toString(self):
        # TODO
        print(self.name)
        print(self.certificates)
