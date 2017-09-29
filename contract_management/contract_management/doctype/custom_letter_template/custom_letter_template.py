# -*- coding: utf-8 -*-
# Copyright (c) 2017, DOKOS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe.utils.jinja import validate_template
from six import string_types

class CustomLetterTemplate(Document):
	def validate(self):
		validate_template(self.template_text)

@frappe.whitelist()
def get_custom_letter_template(template_name, doc):
	if isinstance(doc, string_types):
		doc = json.loads(doc)

	letter_template = frappe.get_doc("Custom Letter Template", template_name)
	return {"letter" : frappe.render_template(letter_template.template_text, doc)}
