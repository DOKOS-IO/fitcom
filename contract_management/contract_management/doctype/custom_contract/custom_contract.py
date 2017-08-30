# -*- coding: utf-8 -*-
# Copyright (c) 2017, DOKOS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class CustomContract(Document):
	def autoname(self):
		if self.contract_series=="Customer":
			series = "Con-{0}-{1}-{2}-".format(self.customer_name, self.issue_date, "C")
			self.naming_series = series

		elif self.contract_series=="Supplier":
			series = "Con-{0}-{1}-{2}-".format(self.supplier_name, self.issue_date, "S")
			self.naming_series = series

		elif self.contract_series=="Employee":
			series = "Con-{0}-{1}-{2}-".format(self.employee_name, self.issue_date, "E")
			self.naming_series = series

		elif self.contract_series=="Sales Partner":
			series = "Con-{0}-{1}-{2}-".format(self.employee_name, self.issue_date, "SP")
			self.naming_series = series


		make_autoname(self.naming_series+'.#####')

	def onload(self):
		pass

	def validate(self):
		self.refresh_financials()
		self.render_template()

	def refresh_financials(self):
		self.quotation_total()
		self.sales_order_total()
		self.sales_invoice_total()
		self.supplier_quotation_total()
		self.purchase_order_total()
		self.purchase_invoice_total()
		frappe.db.commit()

	def quotation_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabQuotation` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		frappe.db.set_value("Custom Contract", self.name, "total_quotation", total[0]["total"])

	def sales_order_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabSales Order` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		frappe.db.set_value("Custom Contract", self.name, "total_sales_order", total[0]["total"])

	def sales_invoice_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabSales Invoice` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		frappe.db.set_value("Custom Contract", self.name, "total_invoiced", total[0]["total"])

	def supplier_quotation_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabSupplier Quotation` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		frappe.db.set_value("Custom Contract", self.name, "total_quotation", total[0]["total"])

	def purchase_order_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabPurchase Order` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		frappe.db.set_value("Custom Contract", self.name, "total_sales_order", total[0]["total"])

	def purchase_invoice_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabPurchase Invoice` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		frappe.db.set_value("Custom Contract", self.name, "total_invoiced", total[0]["total"])

	def render_template(self):
		if self.contract_template:
			template = frappe.get_doc("Custom Contract Template", self.contract_template)
			context = get_context(self)

			print(template.template_text)
			rendered_template = frappe.render_template(template.template_text, context)
			frappe.db.set_value("Custom Contract", self.name, "rendered_contract_template", rendered_template)

def get_context(doc):
	return { "doc": doc }
