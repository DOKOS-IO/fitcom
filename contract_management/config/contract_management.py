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
                    "name": "Custom Letter",
                    "label": _("Letter"),
                    "description": _("Letter"),

                },
                {
                    "type": "doctype",
                    "name": "Custom Letter Template",
                    "label": _("Letter Template"),
                    "description": _("Letter Template"),
                },
            ]
        },
        {
            "label": _("Bonds"),
            "icon": "icon-star",
            "items": [
                    {
                        "type": "doctype",
                        "name": "Custom Contract Bond",
                        "label": _("Bonds"),
                        "description": _("Bonds"),

                    }
            ]
        }
    ]
