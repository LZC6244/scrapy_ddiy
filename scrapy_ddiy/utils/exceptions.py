# -*- coding: utf-8 -*-


class WarnMessage(Exception):
    """When user want to send some warning messages, raise this error"""

    def __init__(self, warn_msg: str):
        self.warn_msg = warn_msg
