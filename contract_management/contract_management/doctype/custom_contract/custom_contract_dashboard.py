from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on documents linked to this contract'),
		'fieldname': 'custom_contract',
		'transactions': [
			{
				'label': _('Sales'),
				'items': ['Quotation', 'Sales Order','Sales Invoice']
			},
			{
				'label': _('Purchases'),
				'items': ['Purchase Order', 'Purchase Invoice']
			}
		]
	}
