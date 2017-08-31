// Copyright (c) 2017, DOKOS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Contract', {
	refresh: function(frm) {

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
	},
	contract_template: function(frm) {
		if (frm.doc.contract_template!=null){
			frm.doc.contract_title = frm.doc.contract_template;
		}
	},
	party_address: function(frm){
		frappe.call({
			method: "frappe.contacts.doctype.address.address.get_address_display",
			args: {"address_dict": frm.doc.party_address },
			callback: function(r) {
				if(r.message) {
					console.log(r.message);
					frm.set_value("address_display", r.message);
				}
			}
		})
	}
});
