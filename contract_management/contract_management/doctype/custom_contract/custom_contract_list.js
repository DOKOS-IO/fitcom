frappe.listview_settings['Custom Contract'] = {
	add_fields: ["contract_status"],
	get_indicator: function(doc) {
		var indicator = [__(doc.contract_status), frappe.utils.guess_colour(doc.contract_status), "status,=," + doc.contract_status];
		indicator[1] = {"Open": "green", "To be Renewed": "orange", "Renewal": "green", "Suspend": "red","Terminated": "darkgrey"}[doc.contract_status];
		return indicator;
	}
};
