# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
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

import yagmail

from smtplib import SMTPAuthenticationError
from os import path
from typing import Optional
from tempfile import mkdtemp
from neon_utils.file_utils import decode_base64_string_to_file
from neon_utils.logger import LOG
from neon_utils.configuration_utils import NGIConfig

CONFIG = NGIConfig("ngi_auth_vars", "/config").get("emails")


def write_out_email_attachments(attachments: dict) -> list:
    """
    Write out email attachments to local files
    :param attachments: dict of attachment file names to string-encoded bytes
    :return: list of paths to attachment files
    """
    att_files = []
    # Write out attachment message data to files
    if attachments:
        LOG.debug("Handling attachments")
        for att_name, data in attachments.items():
            if not data:
                continue
            temp_dir = mkdtemp()
            file_name = path.join(temp_dir, att_name)
            filename = decode_base64_string_to_file(data, file_name)
            att_files.append(filename)
    return att_files


def send_ai_email(subject: str, body: str, recipient: str,
                  attachments: Optional[list] = None, email_config: dict = None):
    """
    Email a user. Email config may be provided or read from configuration
    :param subject: Email subject
    :param body: Email body
    :param recipient: Recipient email address (or list of email addresses)
    :param attachments: Optional list of attachment file paths
    :param email_config: Optional SMTP config to use as sender
    """
    config = email_config or CONFIG
    try:
        mail = config['mail']
        password = config['pass']
        host = config['host']
        port = config['port']
    except (TypeError, KeyError):
        LOG.error(f"Invalid Config: {config}")
        raise RuntimeError("Invalid email auth config")
    LOG.debug(f"send {subject} to {recipient}")
    try:
        with yagmail.SMTP(mail, password, host, port) as yag:
            yag.send(to=recipient, subject=subject, contents=body,
                     attachments=attachments)
    except SMTPAuthenticationError as e:
        LOG.error(f"Invalid credentials provided in config: {config}")
        raise e
