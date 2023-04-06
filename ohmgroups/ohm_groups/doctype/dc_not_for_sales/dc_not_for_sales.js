// Copyright (c) 2023, thirvusoft and contributors
// For license information, please see license.txt
var party_items = []

function itemFilters(frm) {
    
    if (!frm.doc.party || !frm.doc.party_type) {
        party_items = []
        return
    }
    frappe.db.get_value('Supplier', { 'name': frm.doc.party }, 'default_item', (r) => {
        if (r.default_item == 1) {
            frm.call({
                method: "item_supplier",
                args: {
                    party: frm.doc.party,
                },
                callback: function (r) {
                    party_items = r.message || []
                    frm.set_query("item_code", "items", function () {
                        return {
                            filters: {
                                "item_code": ["in", r.message]
                            }

                        }
                    })
                }
            })

        }

    })
    frappe.db.get_value('Customer', { 'name': frm.doc.party }, '_default_item', (r) => {
        if (r._default_item == 1) {
            frm.call({
                method: "item_customer",
                args: {
                    party: frm.doc.party,
                },
                callback: function (r) {
                    party_items = r.message || []
                    frm.set_query("item_code", "items", function () {
                        return {
                            filters: {
                                "item_code": ["in", r.message]
                            }

                        }
                    })
                }
            })

        }

    })
}
frappe.ui.form.on('DC Not for Sales', {
    refresh: function (frm) {
        itemFilters(frm)
        frm.set_query("party_type", function () {
            return {
                filters: {
                    "name": ["in", ["Customer", "Supplier"]]
                }

            }
        }),
        frm.set_query("item_code","items",function(){
            return {
                filters:{
                    "has_variants":0
                }
                
            }
        })
            frm.set_query("transporter", function () {
                return {
                    filters: {
                        is_transporter: 1
                    }
                };
            });
        if (!frm.doc.branch) {
            frm.call({

                method: "address_company",
                args: {
                    company: frm.doc.company,
                },

                callback: function (r) {
                    frm.set_value("company_address", r.message)
                }
            })
        }

        // frm.add_custom_button(
        //     __("Generate"),
        //     () => show_generate_e_waybill_dialog(frm),
        //     "e-Waybill"
        // );



    },






    // setup(frm) {
    //     frm.call({

    //         method: "address_company",
    //         args:{
    //             company:frm.doc.company,
    //         },

    //         callback: function(r) {
    //             frm.set_value("company_address",r.message)
    //     }
    //     })
    // },
    mode_of_transport(frm) {
        frm.set_value("gst_vehicle_type", get_vehicle_type(frm.doc));
    },
    branch(frm) {
        frm.call({

            method: "branch_address_company",
            args: {
                company: frm.doc.company,
                branch: frm.doc.branch,
            },
            callback: function (r) {
                cur_frm.set_value("company_address", r.message)

            }
        })
    },

    party: function (frm) {
        frm.set_value("party_name", frm.doc.party)
        frm.call({

            method: "on_insert",
            args: {
                party: frm.doc.party,
            },
            callback: function (r) {
                cur_frm.set_value("warehouse", r.message)

            }
        }),
        itemFilters(frm)
            frm.call({

                method: "address_shipping",
                args: {
                    party_type: frm.doc.party_type,
                    party: frm.doc.party,
                },

                callback: function (r) {
                    frm.set_value("shipping_address_name", r.message)
                }
            }),
            frm.call({

                method: "address_billing",
                args: {
                    party_type: frm.doc.party_type,
                    party: frm.doc.party,
                },

                callback: function (r) {
                    frm.set_value("customer_address", r.message)
                }
            })

    },

})
function show_generate_e_waybill_dialog(frm) {
    const generate_action = values => {
        frappe.call({
            method: "india_compliance.gst_india.utils.e_waybill.generate_e_waybill",
            args: {
                doctype: frm.doctype,
                docname: frm.doc.name,
                values,
            },
            callback: () => frm.refresh(),
        });
    };

    const json_action = async values => {
        const ewb_data = await frappe.xcall(
            "india_compliance.gst_india.utils.e_waybill.generate_e_waybill_json",
            {
                doctype: frm.doctype,
                docnames: frm.doc.name,
                values,
            }
        );

        frm.refresh();
        trigger_file_download(ewb_data, get_e_waybill_file_name(frm.doc.name));
    };

    const fields = [
        {
            label: "Part A",
            fieldname: "section_part_a",
            fieldtype: "Section Break",
        },
        {
            label: "Transporter",
            fieldname: "transporter",
            fieldtype: "Link",
            options: "Supplier",
            default: frm.doc.transporter,
            get_query: () => {
                return {
                    filters: {
                        is_transporter: 1,
                    },
                };
            },
            onchange: () => update_gst_tranporter_id(d),
        },
        {
            label: "Distance (in km)",
            fieldname: "distance",
            fieldtype: "Float",
            default: frm.doc.distance,
            description:
                "Set as zero to update distance as per the e-Waybill portal (if available)",
        },
        {
            fieldtype: "Column Break",
        },
        {
            label: "GST Transporter ID",
            fieldname: "gst_transporter_id",
            fieldtype: "Data",
            default:
                frm.doc.gst_transporter_id && frm.doc.gst_transporter_id.length == 15
                    ? frm.doc.gst_transporter_id
                    : "",
        },
        // Sub Supply Type will be visible here for Delivery Note
        {
            label: "Part B",
            fieldname: "section_part_b",
            fieldtype: "Section Break",
        },

        {
            label: "Vehicle No",
            fieldname: "vehicle_no",
            fieldtype: "Data",
            default: frm.doc.vehicle_no,
            onchange: () => update_generation_dialog(d),
        },
        {
            label: "Transport Receipt No",
            fieldname: "lr_no",
            fieldtype: "Data",
            default: frm.doc.lr_no,
            onchange: () => update_generation_dialog(d),
        },
        {
            label: "Transport Receipt Date",
            fieldname: "lr_date",
            fieldtype: "Date",
            default: frm.doc.lr_date,
            mandatory_depends_on: "eval:doc.lr_no",
        },
        {
            fieldtype: "Column Break",
        },

        {
            label: "Mode Of Transport",
            fieldname: "mode_of_transport",
            fieldtype: "Select",
            options: `\nRoad\nAir\nRail\nShip`,
            default: frm.doc.mode_of_transport,
            onchange: () => {
                update_generation_dialog(d);
                update_vehicle_type(d);
            },
        },
        {
            label: "GST Vehicle Type",
            fieldname: "gst_vehicle_type",
            fieldtype: "Select",
            options: `Regular\nOver Dimensional Cargo (ODC)`,
            depends_on: 'eval:["Road", "Ship"].includes(doc.mode_of_transport)',
            read_only_depends_on: "eval: doc.mode_of_transport == 'Ship'",
            default: frm.doc.gst_vehicle_type,
        },
    ];

    if (frm.doctype === "Delivery Note") {
        const same_gstin = frm.doc.billing_address_gstin == frm.doc.company_gstin;
        let options;

        if (frm.doc.is_return) {
            if (same_gstin) {
                options = ["For Own Use", "Exhibition or Fairs"];
            } else {
                options = ["Job Work Returns", "SKD/CKD"];
            }
        } else {
            if (same_gstin) {
                options = [
                    "For Own Use",
                    "Exhibition or Fairs",
                    "Line Sales",
                    "Recipient Not Known",
                ];
            } else {
                options = ["Job Work", "SKD/CKD"];
            }
        }

        // Inserted at the end of Part A section
        fields.splice(5, 0, {
            label: "Sub Supply Type",
            fieldname: "sub_supply_type",
            fieldtype: "Select",
            options: options.join("\n"),
            default: options[0],
            reqd: 1,
        });
    }

    const api_enabled = ic.is_api_enabled();

    const d = new frappe.ui.Dialog({
        title: __("Generate e-Waybill"),
        fields,
        primary_action_label: get_primary_action_label_for_generation(frm.doc),
        primary_action(values) {
            d.hide();

            if (api_enabled) {
                generate_action(values);
            } else {
                json_action(values);
            }
        },
        secondary_action_label: api_enabled ? __("Download JSON") : null,
        secondary_action: api_enabled
            ? () => {
                d.hide();
                json_action(d.get_values());
            }
            : null,
    });

    d.show();

    // Alert if e-Invoice hasn't been generated
    if (
        frm.doctype === "Delivery Note" &&
        is_e_invoice_applicable(frm) &&
        !frm.doc.irn
    ) {
        $(`
            <div class="alert alert-warning" role="alert">
                e-Invoice hasn't been generated for this Sales Invoice.
                <a
                    href="https://docs.erpnext.com/docs/v14/user/manual/en/regional/india/generating_e_invoice#what-if-we-generate-e-waybill-before-the-e-invoice"
                    class="alert-link"
                    target="_blank"
                >
                    Learn more
                </a>
            </div>
        `).prependTo(d.wrapper);
    }
}
frappe.ui.form.on('DC Items', {

    qty: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'balance_qty', row.qty)
    },
    item_code: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        if (row.item_code && !frm.doc.party) {
            frappe.model.set_value(cdt, cdn, "item_name", "")
            frappe.model.set_value(cdt, cdn, "item_code", "")
            frappe.throw("Kindly fill party")

        }
        frappe.db.get_value('Supplier', { 'name': frm.doc.party }, 'default_item', (r) => {
            if(r.default_item == 1){
                if (row.item_code && !party_items.includes(row.item_code)) {
                    let item_code = row.item_code
                    frappe.model.set_value(cdt, cdn, "item_name", "")
                    frappe.model.set_value(cdt, cdn, "item_code", "")
                    frappe.throw(`<b>${item_code}</b> does not belong to ${frm.doc.party_type} <b>${frm.doc.party}</b>`)
        
                }
            }
        })
        frappe.db.get_value('Customer', { 'name': frm.doc.party }, '_default_item', (r) => {
            if(r._default_item == 1){
                if (row.item_code && !party_items.includes(row.item_code)) {
                    let item_code = row.item_code
                    frappe.model.set_value(cdt, cdn, "item_name", "")
                    frappe.model.set_value(cdt, cdn, "item_code", "")
                    frappe.throw(`<b>${item_code}</b> does not belong to ${frm.doc.party_type} <b>${frm.doc.party}</b>`)
        
                }
            }
        })

    }

})
function get_primary_action_label_for_generation(doc) {
    const label = ic.is_api_enabled() ? __("Generate") : __("Download JSON");

    if (are_transport_details_available(doc)) {
        return label;
    }

    return label + " (Part A)";
}

function are_transport_details_available(doc) {
    return (
        (doc.mode_of_transport == "Road" && doc.vehicle_no) ||
        (["Air", "Rail"].includes(doc.mode_of_transport) && doc.lr_no) ||
        (doc.mode_of_transport == "Ship" && doc.lr_no && doc.vehicle_no)
    );
}

function update_vehicle_type(dialog) {
    dialog.set_value("gst_vehicle_type", get_vehicle_type(dialog.get_values(true)));
}

function get_vehicle_type(doc) {
    if (doc.mode_of_transport == "Road") return "Regular";
    if (doc.mode_of_transport == "Ship") return "Over Dimensional Cargo (ODC)";
    return "";
}
function update_generation_dialog(dialog) {
    const dialog_values = dialog.get_values(true);
    const primary_action_label = get_primary_action_label_for_generation(dialog_values);

    dialog.set_df_property(
        "gst_transporter_id",
        "reqd",
        primary_action_label.includes("Part A") ? 1 : 0
    );

    set_primary_action_label(dialog, primary_action_label);
}
function get_e_waybill_file_name(docname) {
    let prefix = "Bulk";
    if (docname) {
        prefix = docname.replaceAll(/[^\w_.)( -]/g, "");
    }

    return `${prefix}_e-Waybill_Data_${frappe.utils.get_random(5)}.json`;
}

function set_primary_action_label(dialog, primary_action_label) {
    dialog.get_primary_btn().removeClass("hide").html(primary_action_label);
}
async function update_gst_tranporter_id(dialog) {
    const transporter = dialog.get_value("transporter");
    const { message: response } = await frappe.db.get_value(
        "Supplier",
        transporter,
        "gst_transporter_id"
    );

    dialog.set_value("gst_transporter_id", response.gst_transporter_id);
}
function trigger_file_download(file_content, file_name) {
    let type = "application/json;charset=utf-8";

    if (!file_name.endsWith(".json")) {
        type = "application/octet-stream";
    }

    const blob = new Blob([file_content], { type: type });

    // Create a link and set the URL using `createObjectURL`
    const link = document.createElement("a");
    link.style.display = "none";
    link.href = URL.createObjectURL(blob);
    link.download = file_name;

    // It needs to be added to the DOM so it can be clicked
    document.body.appendChild(link);
    link.click();

    // To make this work on Firefox we need to wait
    // a little while before removing it.
    setTimeout(() => {
        URL.revokeObjectURL(link.href);
        link.parentNode.removeChild(link);
    }, 0);
}
function update_vehicle_type(dialog) {
    dialog.set_value("gst_vehicle_type", get_vehicle_type(dialog.get_values(true)));
}

function get_vehicle_type(doc) {
    if (doc.mode_of_transport == "Road") return "Regular";
    if (doc.mode_of_transport == "Ship") return "Over Dimensional Cargo (ODC)";
    return "";
}