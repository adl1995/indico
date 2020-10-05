# This file is part of Indico.
# Copyright (C) 2002 - 2020 CERN
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see the
# LICENSE file for more details.

from __future__ import unicode_literals

from datetime import datetime, time

from flask import flash, redirect, render_template, request, session, json, jsonify
from webargs import fields

from indico.web.args import use_kwargs
from indico.web.rh import RH
from indico.web.util import jsonify_data, jsonify_template, url_for_index
from indico.legacy.common.cache import GenericCache

from uuid import uuid4

class RHPrepareEvent(RH):
    """Prepare a new event, store it using GenericCache util, and create a UUID."""

    CSRF_ENABLED = False
    _cache = GenericCache('event-preparation')

    # def _prepare_event(self, data):
        # self._cache.get(event_key)

    @use_kwargs({
        'create_booking': fields.String(missing=''),
        'category': fields.String(missing=''),
        'title': fields.String(missing=''),
        'start_dt': fields.String(missing=''),
        'end_dt': fields.String(missing=''),
        'timezone': fields.String(missing='')
    })
    def _process(self, create_booking, category, title, start_dt, end_dt, timezone):
        print('category: ', category)
        # return jsonify(success='Test')
        # form_cls = EventCreationForm
        # form = form_cls(prefix='event-preparation-')
        event_key = unicode(uuid4())
        self._cache.set(
            event_key,
            {create_booking, category, title, start_dt, end_dt, timezone},
            90
        )
        # self._cache.set(
        #     event_key,
        #     {
        #     "create_booking": create_booking,
        #      "category": category,
        #      "title": title,
        #      "start_dt": start_dt,
        #      "end_dt": end_dt,
        #      "timezone": timezone
        #      },
        #     90
        # )

        # print('Form data: ', form.data)
        #
        # self._cache.set(event_key, form.data, 90)

        return jsonify(uuid=event_key)
