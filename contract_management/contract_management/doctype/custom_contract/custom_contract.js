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

	}
});
