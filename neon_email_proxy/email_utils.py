# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
#
# Copyright 2008-2021 Neongecko.com Inc. | All Rights Reserved
#
# Notice of License - Duplicating this Notice of License near the start of any file containing
# a derivative of this software is a condition of license for this software.
# Friendly Licensing:
# No charge, open source royalty free use of the Neon AI software source and object is offered for
# educational users, noncommercial enthusiasts, Public Benefit Corporations (and LLCs) and
# Social Purpose Corporations (and LLCs). Developers can contact developers@neon.ai
# For commercial licensing, distribution of derivative works or redistribution please contact licenses@neon.ai
# Distributed on an "AS IS” basis without warranties or conditions of any kind, either express or implied.
# Trademarks of Neongecko: Neon AI(TM), Neon Assist (TM), Neon Communicator(TM), Klat(TM)
# Authors: Guy Daniels, Daniel McKnight, Regina Bloomstine, Elon Gasper, Richard Leeds
#
# Specialized conversational reconveyance options from Conversation Processing Intelligence Corp.
# US Patents 2008-2021: US7424516, US20140161250, US20140177813, US8638908, US8068604, US8553852, US10530923, US10530924
# China Patent: CN102017585  -  Europe Patent: EU2156652  -  Patents Pending
from smtplib import SMTPAuthenticationError

import yagmail

from os import path
from typing import Optional
from tempfile import gettempdir
from neon_utils.file_utils import decode_base64_string_to_file
from neon_utils.logger import LOG
from neon_utils.configuration_utils import NGIConfig

CONFIG = NGIConfig("ngi_auth_vars")["emails"]


def write_out_email_attachments(message) -> list:
    """
    Write out email attachments from the passed message and return the list of written files
    :param message: Message associated with email request
    :return: list of paths to attachment files
    """
    email = message.data["email"]
    title = message.data["title"]
    body = message.data["body"]
    attachments = message.data.get("attachments")

    LOG.debug(f"Send {title} to {email}:")
    LOG.debug(body)

    att_files = []
    # Write out attachment message data to files
    if attachments:
        LOG.debug("Handling attachments")
        try:
            for att_name, data in attachments.items():
                if not data:
                    continue
                temp_dir = gettempdir()
                file_name = path.join(temp_dir, att_name)
                filename = decode_base64_string_to_file(data, file_name)
                att_files.append(filename)
        except Exception as e:
            LOG.error(e)
            LOG.error(attachments.keys())
    return att_files


def send_ai_email(title: str, body: str, recipient: str, att_files: Optional[list] = None, email_config: dict = None):
    """
    Send an email to a user. Email config may be provided or read from configuration
    :param title: Email subject
    :param body: Email body
    :param recipient: Recipient email address (or list of email addresses)
    :param att_files: Optional list of attachment file paths
    :param email_config: Optional SMTP config to use as sender
    """
    config = email_config or CONFIG
    mail = config['mail']
    password = config['pass']
    host = config['host']
    port = config['port']
    LOG.debug(f"send {title} to {recipient}")
    try:
        with yagmail.SMTP(mail, password, host, port) as yag:
            yag.send(to=recipient, subject=title, contents=body, attachments=att_files)
    except SMTPAuthenticationError:
        LOG.error(f"Invalid credentials provided in config: {config}")
