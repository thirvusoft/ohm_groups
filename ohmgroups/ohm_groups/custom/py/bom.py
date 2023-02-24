import frappe

def auto_fg_item(doc, actions):
    fg_item = frappe.get_doc("Item",{"name":doc.item})
    if fg_item.has_variants == 1:
        item = frappe.get_all("Item Variant Attribute",filters={"variant_of":doc.item},fields=["parent","attribute_value"])
        for i in item:
            if i.attribute_value == "Fg":
                    doc.item = i.parent
                    doc.item_name = i.parent

@frappe.whitelist()
def operations_(item):
    count = 0
    oper_ = []
    m = []
    items = ""
    v= item.split('-')
    if v[-1] != "FG":
        fg_item = frappe.get_doc("Item",{"name":item})
        if fg_item.has_variants == 1:
            item = frappe.get_all("Item Variant Attribute",filters={"variant_of":["in",item], "attribute_value":["=","Fg"]},fields=["parent","attribute_value"])
            for i in item:
                items =i.parent
            # items.append({"item":i.parent})
                    # item = i.parent
                    # item_name = i.parent
    else:
        items = item 
        
    variant_of = frappe.get_all("Item",filters = {"name":items}, pluck = "parent_item")
    parent = variant_of
    while(True):
        count+=1
        parent_1 = []
        for j in parent:
            parent_1 += frappe.get_all("Item",filters = {"parent_item":j,"is_group":1}, pluck = "name")
            
        variant_of += parent_1
        parent = parent_1
        if len(parent_1) == 0 or count > 500:
            break
    item_code_ = frappe.get_all("Item",filters={"variant_of":["in",variant_of], "attribute_value":["!=","Fg"]},pluck="name") #Get item_code
    attribute_item = frappe.get_all("Item Variant Attribute",filters={"variant_of":["in",variant_of], "attribute_value":["!=","Fg" and "Laser cutting"]},pluck="attribute_value")
    # for i in attribute_item:
        # if not i.attribute_value == "Fg":
    oper_attri = frappe.get_all("Operation",filters={"attributes":["in",attribute_item]},fields = ["name","workstation"],group_by = "name")
    for i in oper_attri:
        oper_.append({"operation":i.name,"workstation":i.workstation})
        m.append(i.name)
        # for d in range(0,len(oper_),1):
        #     for k in range(d+1,)
    return items,oper_,m,item_code_
    # return items
               