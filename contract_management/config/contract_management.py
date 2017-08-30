# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
            "label": _("Contracts"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Custom Contract",
                    "label": _("Contract"),
                    "description": _("Contract"),
                },
                {
                    "type": "doctype",
                    "name": "Custom Contract Template",
                    "label": _("Contract Template"),
                    "description": _("Contract Template"),
                },
                ]
            },
        {
            "label": _("Letters"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Custom Contract",
                    "label": _("Letter"),
                    "description": _("Letter"),

                },
				]
				}
	]
