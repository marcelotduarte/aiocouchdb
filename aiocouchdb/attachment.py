# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

import asyncio
import base64
from .client import Resource


class Attachment(object):
    """Implementation of :ref:`CouchDB Attachment API <api/doc/attachment>`."""

    def __init__(self, url_or_resource):
        if isinstance(url_or_resource, str):
            url_or_resource = Resource(url_or_resource)
        self.resource = url_or_resource

    @asyncio.coroutine
    def exists(self, rev=None, *, auth=None):
        """Checks if `attachment exists`_. Assumes success on receiving response
        with `200 OK` status.

        :param str rev: Document revision
        :param auth: :class:`aiocouchdb.authn.AuthProvider` instance

        :rtype: bool

        .. _attachment exists: http://docs.couchdb.org/en/latest/api/document/attachments.html#head--db-docid-attname
        """
        resp = yield from self.resource.head(auth=auth, params={'rev': rev})
        yield from resp.read()
        return resp.status == 200

    @asyncio.coroutine
    def modified(self, digest, *, auth=None):
        """Checks if `attachment was modified`_ by known MD5 digest.

        :param bytes digest: Attachment MD5 digest. Optionally,
                             may be passed in base64 encoding form
        :param auth: :class:`aiocouchdb.authn.AuthProvider` instance

        :rtype: bool

        .. _attachment was modified: http://docs.couchdb.org/en/latest/api/document/attachments.html#head--db-docid-attname
        """
        if isinstance(digest, bytes):
            if len(digest) != 16:
                raise ValueError('MD5 digest has 16 bytes')
            digest = base64.b64encode(digest).decode()
        elif isinstance(digest, str):
            if not (len(digest) == 24 and digest.endswith('==')):
                raise ValueError('invalid base64 encoded MD5 digest')
        else:
            raise TypeError('invalid `digest` type {}, bytes or str expected'
                            ''.format(type(digest)))
        qdigest = '"%s"' % digest
        resp = yield from self.resource.head(auth=auth,
                                             headers={'IF-NONE-MATCH': qdigest})
        yield from resp.maybe_raise_error()
        yield from resp.read()
        return resp.status != 304