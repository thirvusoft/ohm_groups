from ohmgroups.ohm_groups.utils.stock.quality_inspection import quality_inspection
from ohmgroups.ohm_groups.utils.stock.quality_inspection_reading import property_setter
from ohmgroups.ohm_groups.utils.crm.customers import customers
from ohmgroups.ohm_groups.utils.selling.sales_invoice import sales_invoice
from ohmgroups.ohm_groups.custom.py.workflow import workflow_document_creation
from ohmgroups.ohm_groups.utils.buying.buying import supplier
from ohmgroups.ohm_groups.utils.buying.purchase_order import purchase_order
from ohmgroups.ohm_groups.utils.setup.vehicle import batch_customizations
from ohmgroups.ohm_groups.utils.setup.vehicle_log import batch_customization
from ohmgroups.ohm_groups.utils.setup.driver import driver_custom_fields
from ohmgroups.ohm_groups.utils.stock.quality_inspection_parameter import quality_inspection_paramter
from ohmgroups.ohm_groups.utils.stock.quality_inspection_template import quality_inspection_template
from ohmgroups.ohm_groups.utils.hr.employee import salary_structure_assignment
from ohmgroups.ohm_groups.utils.stock.stock_entry import stock_entry
from ohmgroups.ohm_groups.utils.branch.branch import branch
from ohmgroups.ohm_groups.utils.stock.material_request import material_request
from ohmgroups.ohm_groups.utils.manufacturing.bom import bom
from ohmgroups.ohm_groups.utils.manufacturing.operation import operation
from ohmgroups.ohm_groups.utils.manufacturing.work_order import workorder


def after_install():
    quality_inspection()
    customers()
    property_setter()
    sales_invoice()
    workflow_document_creation()
    supplier()
    purchase_order()
    batch_customizations()
    batch_customization()
    driver_custom_fields()
    quality_inspection_paramter()
    quality_inspection_template()
    stock_entry()
    salary_structure_assignment()
    branch()
    material_request()
    bom()
    operation()
    workorder()
