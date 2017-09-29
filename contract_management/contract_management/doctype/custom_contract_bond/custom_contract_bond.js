// Copyright (c) 2017, DOKOS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Contract Bond', {
	refresh: function(frm) {
		if (frm.doc.collection_date) {
		frappe.call({
			method: "contract_management.contract_management.doctype.custom_contract.custom_contract.change_bond_status",
			args: {"bond": frm.doc.name },
			callback: function(r) {
				if(r.message) {
					frm.set_value("bond_amount", r.message);
				}
			}
		})
	}
}
});
