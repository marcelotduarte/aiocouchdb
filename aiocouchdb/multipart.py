# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

# flake8: noqa

from aiohttp.multipart import (
    MultipartReader,
    MultipartWriter as _MultipartWriter,
    BodyPartReader,
)
from aiocouchdb.hdrs import (
    CONTENT_ENCODING,
    CONTENT_LENGTH,
    CONTENT_TRANSFER_ENCODING,
)


class MultipartWriter(_MultipartWriter):

    def calc_content_length(self):
        total = 0
        len_boundary = len(self.boundary)
        for part in self._parts:
            total += len_boundary + 4  # -- and \r\n
            total += part.calc_content_length()
        total += len_boundary + 6  # -- and --\r\n
        return total
