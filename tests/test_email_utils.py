# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2021 Neongecko.com Inc.
# BSD-3
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import unittest

from mycroft_bus_client import Message

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from neon_email_proxy.email_utils import *

test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_email_attachments")


class TestEmailUtils(unittest.TestCase):
    def test_write_out_email_attachments(self):
        from neon_utils.file_utils import encode_file_to_base64_string
        attachments = {file: encode_file_to_base64_string(os.path.join(test_path, file))
                       for file in os.listdir(test_path)}
        files = write_out_email_attachments(Message("test", {"email": "test@neongecko.com",
                                                             "title": "Test Email Title",
                                                             "body": "Test Email Body",
                                                             "attachments": attachments}))
        for file in files:
            with open(file) as attachment:
                att_contents = attachment.read()
            with open(os.path.join(test_path, os.path.basename(file))) as original:
                original_contents = original.read()
            self.assertEqual(att_contents, original_contents)

    def test_write_out_email_attachments_empty(self):
        attachments = {"test": None}
        files = write_out_email_attachments(Message("test", {"email": "test@neongecko.com",
                                                             "title": "Test Email Title",
                                                             "body": "Test Email Body",
                                                             "attachments": attachments}))
        self.assertEqual(files, list())

    def test_send_ai_email_invalid(self):
        with self.assertRaises(RuntimeError):
            send_ai_email("Testing", "This is an automated unit test", "daniel@neongecko.com",
                          email_config={"mail": "daniel@neongecko.com"})
        with self.assertRaises(SMTPAuthenticationError):
            send_ai_email("Testing", "This is an automated unit test", "daniel@neongecko.com",
                          email_config={"mail": "daniel@neongecko.com",
                                        "pass": "invalid",
                                        "host": "smtp.gmail.com",
                                        "port": "465"})


if __name__ == '__main__':
    unittest.main()
