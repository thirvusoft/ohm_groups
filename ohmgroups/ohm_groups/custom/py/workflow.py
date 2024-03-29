import frappe

def workflow_document_creation():
    create_state()
    create_action()
    create_supplier_flow()
    create_quality_inspection_flow()
    create_laser_cutting_flow()

def create_supplier_flow():
    if frappe.db.exists('Workflow', 'New Supplier Approval'):
        frappe.delete_doc('Workflow', 'New Supplier Approval')
    workflow = frappe.new_doc('Workflow')
    workflow.workflow_name = 'New Supplier Approval'
    workflow.document_type = 'Supplier'
    workflow.workflow_state_field = 'workflow_state'
    workflow.is_active = 1
    workflow.send_email_alert = 1
    workflow.append('states', dict(
        state = 'Pending', allow_edit = 'All',doc_status = 0,update_field = 'disabled',update_value=1,
    ))
    workflow.append('states', dict(
        state = 'Approved', allow_edit = 'System Manager',doc_status = 0,update_field = 'disabled',update_value=0,
    ))
    workflow.append('states', dict(
        state = 'Rejected', allow_edit = 'System Manager',doc_status = 0,update_field = 'disabled',update_value=1,
    )) 
    
    workflow.append('transitions', dict(
        state = 'Pending', action='Approve', next_state = 'Approved',
        allowed='System Manager', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Pending', action='Reject', next_state = 'Rejected',
        allowed='System Manager', allow_self_approval= 1,
    ))
    workflow.insert(ignore_permissions=True)
    return workflow
def create_state():
    list={"Pending":"Warning","Approved":"Success", "Rejected":"Danger"}
    for row in list:
        if not frappe.db.exists('Workflow State', row):
            new_doc = frappe.new_doc('Workflow State')
            new_doc.workflow_state_name = row
            new_doc.style=list[row]
            new_doc.save()



def create_quality_inspection_flow():
    if frappe.db.exists('Workflow', 'Quality Inspection'):
        frappe.delete_doc('Workflow', 'Quality Inspection')
    workflow = frappe.new_doc('Workflow')
    workflow.workflow_name = 'Quality Inspection'
    workflow.document_type = 'Quality Inspection'
    workflow.workflow_state_field = 'workflow_state'
    workflow.is_active = 0
    workflow.send_email_alert = 1
    workflow.append('states', dict(
        state = 'Pending', allow_edit = 'All',doc_status = 0,
    ))
    workflow.append('states', dict(
        state = 'Approved', allow_edit = 'System Manager',doc_status = 1,
    ))
    workflow.append('states', dict(
        state = 'Rejected', allow_edit = 'System Manager',doc_status = 1,

    ))
    workflow.append('states', dict(
        state = 'Cancelled', allow_edit = 'All',doc_status = 2,

    )) 
    
    workflow.append('transitions', dict(
        state = 'Pending', action='Approve', next_state = 'Approved',
        allowed='System Manager', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Pending', action='Reject', next_state = 'Rejected',
        allowed='System Manager', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Approved', action='Cancel', next_state = 'Cancelled',
        allowed='All', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Rejected', action='Cancel', next_state = 'Cancelled',
        allowed='All', allow_self_approval= 1,
    ))
    workflow.insert(ignore_permissions=True)
    return workflow
def create_state():
    list={"Pending":"Warning","Approved":"Success", "Rejected":"Danger","Cancelled":"Warning"}
    for row in list:
        if not frappe.db.exists('Workflow State', row):
            new_doc = frappe.new_doc('Workflow State')
            new_doc.workflow_state_name = row
            new_doc.style=list[row]
            new_doc.save()
           
def create_action():
    list=['Cancel']
    for row in list:
        if not frappe.db.exists('Workflow Action Master', row):
            new_doc = frappe.new_doc('Workflow Action Master')
            new_doc.workflow_action_name = row
            new_doc.save()


def create_laser_cutting_flow():
    if frappe.db.exists('Workflow', 'Laser Cutting'):
        frappe.delete_doc('Workflow', 'Laser Cutting')
    workflow = frappe.new_doc('Workflow')
    workflow.workflow_name = 'Laser Cutting'
    workflow.document_type = 'Laser Cutting'
    workflow.workflow_state_field = 'workflow_state'
    workflow.is_active = 1
    workflow.send_email_alert = 1
    workflow.append('states', dict(
        state = 'Draft', allow_edit = 'All',doc_status = 0,
    ))
    workflow.append('states', dict(
        state = 'Open', allow_edit = 'All',doc_status = 0,
    ))
    workflow.append('states', dict(
        state = 'Send to Laser Cutting', allow_edit = 'All',doc_status = 0,
    ))
    workflow.append('states', dict(
        state = 'Laser Cutting Finished', allow_edit = 'All',doc_status = 0,
    ))
    workflow.append('states', dict(
        state = 'Job Completed', allow_edit = 'All',doc_status = 1,
    ))
    workflow.append('states', dict(
        state = 'Cancelled', allow_edit = 'All',doc_status = 2,

    )) 
    
    workflow.append('transitions', dict(
        state = 'Draft', action='Send to Laser Cutting', next_state = 'Send to Laser Cutting',
        allowed='All', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Send to Laser Cutting', action='Laser Cutting Finished', next_state = 'Laser Cutting Finished',
        allowed='All', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Laser Cutting Finished', action='Job Completed', next_state = 'Job Completed',
        allowed='All', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Job Completed', action='Cancel', next_state = 'Cancelled',
        allowed='All', allow_self_approval= 1,
    ))

    workflow.insert(ignore_permissions=True)
    return workflow
def create_state():
    list={"Draft":"Primary","Send to Laser Cutting":"Primary","Job Completed":"Success", "Rejected":"Danger","Cancelled":"Warning","Open":"Primary","Laser Cutting Finished":"Primary"}
    for row in list:
        if not frappe.db.exists('Workflow State', row):
            new_doc = frappe.new_doc('Workflow State')
            new_doc.workflow_state_name = row
            new_doc.style=list[row]
            new_doc.save()
           
def create_action():
    list=['Job Completed','Send to Laser Cutting','Laser Cutting Finished','Cancel']
    for row in list:
        if not frappe.db.exists('Workflow Action Master', row):
            new_doc = frappe.new_doc('Workflow Action Master')
            new_doc.workflow_action_name = row
            new_doc.save()

def execute():
    workflow_document_creation()