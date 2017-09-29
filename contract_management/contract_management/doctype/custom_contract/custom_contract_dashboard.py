from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on documents linked to this contract'),
		'internal_links': {
			'Project': ['project', 'project'],
		},
		'fieldname': 'custom_contract',
		'transactions': [
			{
				'label': _('Projects'),
				'items': ['Project']
			},
			{
				'label': _('Bonds'),
				'items': ['Custom Contract Bond']
			}
		]
	}
