# -*- coding: utf-8 -*-
# Copyright (c) 2017, DOKOS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from dateutil import relativedelta as rdelta
import datetime
from frappe.utils import getdate

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

	def onload(self):
		pass

	def validate(self):
		self.duration_calculation()
		self.refresh_financials()
		self.render_template()

	def refresh_financials(self):
		self.quotation_total()
		frappe.db.commit()

	def quotation_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabQuotation`""", as_dict=True)
		self.total_quotation = total[0].total

	def sales_order_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabSales Order` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		self.total_quotation = total[0].total

	def sales_invoice_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabSales Invoice` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		self.total_quotation = total[0].total

	def supplier_quotation_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabSupplier Quotation` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		self.total_quotation = total[0].total

	def purchase_order_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabPurchase Order` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		self.total_quotation = total[0].total

	def purchase_invoice_total(self):
		total = frappe.db.sql("""SELECT SUM(total) as total FROM `tabPurchase Invoice` WHERE custom_contract = '{0}'""".format(self.name), as_dict=True)
		self.total_quotation = total[0].total

	def render_template(self):
		if self.contract_template:
			template = frappe.get_doc("Custom Contract Template", self.contract_template)
			context = get_context(self)

			print(template.template_text)
			rendered_template = frappe.render_template(template.template_text, context)
			self.rendered_contract_template = rendered_template

	def duration_calculation(self):
		start_date = getdate(self.contract_start_date)
		end_date = getdate(self.contract_end_date)
		rd = rdelta.relativedelta(end_date, start_date)
		self.contract_duration = "{0.years} years and {0.months} months and {0.days} days".format(rd)

def get_context(doc):
	return { "doc": doc }
