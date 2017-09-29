// Copyright (c) 2017, DOKOS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Letter', {
	onload: function(frm){
		refresh_dynamic_links(frm);
		setup_queries(frm);
	},
	refresh: function(frm) {
	},
	template_name: function(frm) {
		update_letter(frm);
	},
	refresh_template: function(frm) {
		update_letter(frm);
	},
	customer_supplier: function(frm) {
		refresh_dynamic_links(frm);
		setup_queries(frm);
	}
});

var update_letter = function(frm) {
	frappe.call({
		method: 'contract_management.contract_management.doctype.custom_letter_template.custom_letter_template.get_custom_letter_template',
		cache: false,
		args: {
			template_name: frm.doc.template_name,
			doc: me.frm.doc
		},
		callback: function(r) {
			frm.set_value("rendered_letter_template", r.message.letter);
		}
	});
}

var setup_queries = function(frm) {
		frm.set_query('contact_name', erpnext.queries.contact_query);
}

var refresh_dynamic_links = function(frm) {
	if (frm.doc.customer_supplier == "Supplier"){
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'supplier_name', doctype: 'Supplier'};
	}else if (frm.doc.customer_supplier == "Customer"){
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'customer_name', doctype: 'Customer'};
	}
}
