import frappe

def workflow_document_creation():
    create_state()
    create_action()
    create_quotation_flow()

def create_quotation_flow():
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
        state = 'Approved', allow_edit = 'Administrator',doc_status = 0,update_field = 'disabled',update_value=0,
    ))
    workflow.append('states', dict(
        state = 'Rejected', allow_edit = 'Administrator',doc_status = 0,update_field = 'disabled',update_value=1,
    )) 
    
    workflow.append('transitions', dict(
        state = 'Pending', action='Approve', next_state = 'Approved',
        allowed='Administrator', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Pending', action='Reject', next_state = 'Rejected',
        allowed='Administrator', allow_self_approval= 1,
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
def create_action():
    pass

def execute():
    workflow_document_creation()