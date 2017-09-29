# -*- coding: utf-8 -*-
# Copyright (c) 2017, DOKOS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe.utils.jinja import validate_template
from six import string_types

class CustomContractTemplate(Document):
	def validate(self):
		validate_template(self.template_text)

@frappe.whitelist()
def get_custom_contract_template(template_name, doc):
	if isinstance(doc, string_types):
		doc = json.loads(doc)

	if ("customer_name" in doc) and (doc["customer_name"] != None):
		customer_name = frappe.get_doc("Customer", doc["customer_name"])
		doc["customer_name"] = customer_name
	else:
		doc["customer_name"] = "Undefined"
	if ("supplier_name" in doc) and (doc["supplier_name"] != None):
		supplier_name = frappe.get_doc("Supplier", doc["supplier_name"])
		doc["supplier_name"] = supplier_name
	else:
		doc["supplier_name"] = "Undefined"
	if ("company_name" in doc) and (doc["company_name"] != None):
		company_name = frappe.get_doc("Company", doc["company_name"])
		doc["company_name"] = company_name
	else:
		doc["company_name"] = "Undefined"
	if ("employee_name" in doc) and (doc["employee_name"] != None):
		employee_name = frappe.get_doc("Employee", doc["employee_name"])
		doc["employee_name"] = employee_name
	else:
		doc["employee_name"] = "Undefined"
	if ("party_contact" in doc) and (doc["party_contact"] != None):
		party_contact = frappe.get_doc("Contact", doc["party_contact"])
		doc["party_contact"] = party_contact
	else:
		doc["party_contact"] = "Undefined"
	if ("sales_partner" in doc) and (doc["sales_partner"] != None):
		sales_partner = frappe.get_doc("Sales Partner", doc["sales_partner"])
		doc["sales_partner"] = sales_partner
	else:
		doc["sales_partner"] = "Undefined"
	if ("party_address" in doc) and (doc["party_address"] != None):
		party_address = frappe.get_doc("Address", doc["party_address"])
		doc["party_address"] = party_address
	else:
		doc["party_address"] = "Undefined"
	if ("company_address" in doc) and (doc["company_address"] != None):
		company_address = frappe.get_doc("Address", doc["company_address"])
		doc["company_address"] = company_address
	else:
		doc["company_address"] = "Undefined"
	if ("contract_owner_name" in doc) and (doc["contract_owner_name"] != None):
		contract_owner_name = frappe.get_doc("Employee", doc["contract_owner_name"])
		doc["contract_owner_name"] = contract_owner_name
	else:
		doc["contract_owner_name"] = "Undefined"
	if ("project_manager" in doc) and (doc["project_manager"] != None):
		project_manager = frappe.get_doc("Employee", doc["project_manager"])
		doc["project_manager"] = project_manager
	else:
		doc["project_manager"] = "Undefined"


	contract_template = frappe.get_doc("Custom Contract Template", template_name)
	return {"contract" : frappe.render_template(contract_template.template_text, doc)}
