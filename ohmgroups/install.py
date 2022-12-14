from ohmgroups.ohm_groups.utils.stock.quality_inspection import quality_inspection
from ohmgroups.ohm_groups.utils.stock.quality_inspection_reading import property_setter
from ohmgroups.ohm_groups.utils.crm.customers import customers
from ohmgroups.ohm_groups.utils.selling.sales_invoice import sales_invoice
from ohmgroups.ohm_groups.custom.py.workflow import workflow_document_creation


def after_install():
    quality_inspection()
    customers()
    property_setter()
    sales_invoice()
    workflow_document_creation()
