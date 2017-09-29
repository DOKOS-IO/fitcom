// Copyright (c) 2017, DOKOS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Contract', {
	onload: function(frm){
		if (frm.doc.contract_series) {
			refresh_dynamic_links(frm);
		}
		if (frm.doc.contract_status=="To be Renewed") {
					frm.dashboard.add_comment(__('Contract to be Renewed before ', frm.doc.contract_end_date), 'orange', true);
		}
		setup_queries(frm);
	},
	refresh: function(frm) {
		if (frm.doc.contract_template!=null){
			if (frm.doc.contract_series == "Supplier"){
				frm.set_value("contract_title", frm.doc.contract_template + "-" + frm.doc.supplier_name);
			}else if (frm.doc.contract_series == "Customer"){
				frm.set_value("contract_title", frm.doc.contract_template + "-" + frm.doc.customer_name);
			}else if (frm.doc.contract_series == "Employee"){
				frm.set_value("contract_title", frm.doc.contract_template + "-" + frm.doc.employee_name);
			}else if (frm.doc.contract_series == "Sales Partner"){
				frm.set_value("contract_title", frm.doc.contract_template + "-" + frm.doc.sales_partner);
			}
		}
	},
	before_submit: function(frm) {
		if (frm.doc.contract_template!=null){
			update_contract(frm);
		}
	},
	contract_series: function(frm) {
		if (frm.doc.contract_series == "Supplier"){
			frm.set_df_property('supplier_name', 'reqd', 1);
		}else if (frm.doc.contract_series == "Customer"){
			frm.set_df_property('customer_name', 'reqd', 1);
		}else if (frm.doc.contract_series == "Employee"){
			frm.set_df_property('employee_name', 'reqd', 1);
		}else if (frm.doc.contract_series == "Sales Partner"){
			frm.set_df_property('sales_partner', 'reqd', 1);
		}
		refresh_dynamic_links(frm);
	},
	contract_template: function(frm) {
		update_contract(frm);
	},
	party_address: function(frm){
		if (frm.doc.party_address) {
		frappe.call({
			method: "frappe.contacts.doctype.address.address.get_address_display",
			args: {"address_dict": frm.doc.party_address },
			callback: function(r) {
				if(r.message) {
					frm.set_value("address_display", r.message);
				}
			}
		})
	}
	},
	company_address: function(frm){
		if (frm.doc.company_address) {
		frappe.call({
			method: "frappe.contacts.doctype.address.address.get_address_display",
			args: {"address_dict": frm.doc.company_address },
			callback: function(r) {
				if(r.message) {
					frm.set_value("company_address_display", r.message);
				}
			}
		})
		setup_queries(frm);
	}
	},
	refresh_template: function(frm){
		update_contract(frm);
	}
});

var update_contract = function(frm) {
	frappe.call({
		method: 'contract_management.contract_management.doctype.custom_contract_template.custom_contract_template.get_custom_contract_template',
		args: {
			template_name: frm.doc.contract_template,
			doc: me.frm.doc
		},
		callback: function(r) {
			frm.set_value("rendered_contract_template", r.message.contract);
		}
	});
}

var setup_queries = function(frm) {
		frm.set_query('party_contact', erpnext.queries.contact_query);
		frm.set_query('party_address', erpnext.queries.address_query);
		frm.set_query('company_address', function() {
			if(!frm.doc.company_name) {
				return;
			}
			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Company',
					link_name: frm.doc.company_name
				}
			};
		});
}

var refresh_dynamic_links = function(frm) {
	if (frm.doc.contract_series == "Supplier"){
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'supplier_name', doctype: 'Supplier'};
	}else if (frm.doc.contract_series == "Customer"){
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'customer_name', doctype: 'Customer'};
	}else if (frm.doc.contract_series == "Employee"){
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'employee_name', doctype: 'Employee'};
	}else if (frm.doc.contract_series == "Sales Partner"){
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'sales_partner', doctype: 'Sales Partner'};
	}
}
