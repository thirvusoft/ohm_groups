// Copyright (c) 2023, thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Laser Cutting', {
    refresh: function (frm) {
        let fields = []
        if (frm.doc.frozen == 1) {
            for (let i = 0; i < frappe.get_meta('Laser Cutting').fields.length; i++) {
                if (frappe.get_meta('Laser Cutting').fields[i].fieldname == 'job_work_tab') { break; }
                fields.push(frappe.get_meta('Laser Cutting').fields[i].fieldname)
                frm.set_df_property(frappe.get_meta('Laser Cutting').fields[i].fieldname, 'read_only', 1)
            }
        }
        //    if(frm.doc.number_of_sheets){
        //     frm.call({

        //         method: "set_time_log",
        //         args: {
        //             number_of_sheets: frm.doc.number_of_sheets,
        //             designation: frm.doc.designation,
        //             designation_2: frm.doc.designation_2,
        //             operators:frm.doc.operators,
        //             helpers: frm.doc.helpers
        //         },
        //         callback: function (r) {
        //                 frm.set_value("time_logs",r.message[0])
        //                 frm.events.start_job(frm, "Work In Progress",r.message[0]);


        //         }
        //     });
        //    }

        if (frm.doc.laser_cutting[0].qty) {
            frm.call({
                method: "sheet_no",
                args: {
                    laser_cutting: frm.doc.laser_cutting
                },
                callback: function (r) {
                    // frm.reload_doc();
                    frm.set_df_property('number_of_sheets', 'options', r.message)
                }
            });
        }

        frm.trigger("make_dashboard");
        if (!frm.is_new() && frm.doc.docstatus == 0 && !(frm.doc.total_qty == frm.doc.total_completed_qty)) {
            {
                if (!frm.doc.started_time && !frm.doc.current_time) {
                    frm.add_custom_button(__("Start Job"), async () => {
                        // if ((frm.doc.employee && !frm.doc.employee.length) || !frm.doc.employee) {
                        // frappe.prompt({fieldtype: 'Table MultiSelect', label: __('Select Employees'),
                        //     options: "Laser Cutting Time Log", fieldname: 'employees'}, d => {
                        //     frm.events.start_job(frm, "Work In Progress", d.employees);
                        //     frm.set_value("status",frm.doc.status)
                        // }, __("Assign Job to Employee"));
                        // if(frm.doc.number_of_sheets == ""){
                        //     frappe.throw("Hii")
                        // }
                        // return
                        //  if(!frm.doc.number_of_sheets){
                        //     frappe.throw("Kindly Select the Number of Sheets")

                        // }


                        await frm.call({

                            method: "set_time_log",
                            args: {
                                number_of_sheets: frm.doc.number_of_sheets,
                                designation: frm.doc.designation,
                                designation_2: frm.doc.designation_2,
                                operators: frm.doc.operators,
                                helpers: frm.doc.helpers
                            },
                            callback: function (r) {
                                if (!frm.doc.number_of_sheets) {
                                    frappe.throw("Kindly Select the Number of Sheets")

                                }
                                frm.set_value("time_logs", r.message)
                                frm.events.start_job(frm, "Work In Progress", r.message);


                            }
                        });


                        //     } else {
                        //         frm.events.start_job(frm, "Work In Progress", frm.doc.employee);
                        //     }
                        // }).addClass("btn-primary");
                        frm.set_value("number_of_sheets", "")
                        frm.set_value("designation", "")
                        frm.set_value("designation_2", "")
                        frm.set_value("operators", [])
                        frm.set_value("helpers", [])
                        frm.refresh_fields("number_of_sheets")
                    })
                } else if (frm.doc.status == "On Hold") {
                    frm.add_custom_button(__("Resume Job"), () => {
                        frm.events.start_job(frm, "Resume Job", frm.doc.employee);
                    }).addClass("btn-primary");
                } else {
                    // frm.add_custom_button(__("Pause Job"), () => {
                    //     frm.events.complete_job(frm, "On Hold");
                    // });

                    frm.add_custom_button(__("Complete Job"), () => {
                        var sub_operations = frm.doc.sub_operations;

                        let set_qty = true;
                        if (sub_operations && sub_operations.length > 1) {
                            set_qty = false;
                            let last_op_row = sub_operations[sub_operations.length - 2];

                            if (last_op_row.status == 'Complete') {
                                set_qty = true;
                            }
                        }
                        // frm.events.complete_job(frm, "Complete", 0.0);

                        //     let fields = [];

                        // frappe.call({
                            // method: 'ohmgroups.ohm_groups.doctype.laser_cutting.laser_cutting.item_table',
                            // args: {
                            //     raw_materials: frm.doc.raw_materials
                            // },
                            // callback(r) {
                                let table = [
                                    {
                                        'fieldname': 'sheet_no',
                                        'label': 'Sheet No',
                                        'fieldtype': 'Data',
                                        'in_list_view': 1,
                                        'read_only': 1,
                                        'column': 2
                                    },
                                    {
                                        'fieldname': 'item_code',
                                        'label': 'Item Code',
                                        'fieldtype': 'Link',
                                        'options': 'Item',
                                        'in_list_view': 1,
                                        'read_only': 1,
                                        'column': 2
                                    },
                                    {
                                        'fieldname': 'actual_qty',
                                        'label': 'Actual Qty',
                                        'fieldtype': 'Float',
                                        'in_list_view': 1,
                                        'read_only': 1,
                                        'column': 1
                                    },
                                    {
                                        'fieldname': 'rejected_qty',
                                        'label': 'Rejected Qty',
                                        'fieldtype': 'Float',
                                        'in_list_view': 1,
                                        'column': 1
                                    },
                                    {
                                        'fieldname': 'accepted_qty',
                                        'label': 'Accepted Qty',
                                        'fieldtype': 'Float',
                                        'in_list_view': 1,
                                        'column': 1
                                    },
                                    {
                                        'fieldname': 'missing_qty',
                                        'label': 'Missing Qty',
                                        'fieldtype': 'Float',
                                        'in_list_view': 1,
                                        'column': 1

                                    },
                                    {
                                        'fieldname': 'remark',
                                        'fieldtype': 'Small Text',
                                        'label': 'Remark',
                                        'in_list_view': 1,
                                        'column': 2
                                    }
                                ]
                                let item = []
                                console.log("------")
                                console.log(frm.doc.number_of_sheets)
                                frm.doc.raw_materials.forEach((i) => {
                                    item.push({ "item_code": i.item_code, "actual_qty": i.per_sheet_qty,"sheet_no":frm.doc.time_logs[frm.doc.time_logs.length-1]?.sheet_no})
                                })

                                var d = new frappe.ui.Dialog({
                                    title: 'Complete Job',
                                    size: 'large',
                                    minimizable: true,
                                    static: true,
                                    fields: [
                                        {
                                            fieldname: 'table',
                                            fieldtype: 'Table',
                                            fields: table,
                                            data: item,
                                            cannot_add_rows: 1,
                                        }
                                    ],
                                    primary_action_label: 'Submit',
                                    secondary_action_label: 'Close',
                                    async primary_action(data) {
                                        if (data.table) {
                                            await frm.events.complete_job(frm, "Complete", data.table);

                                        }
                                        frm.reload_doc()
                                        d.hide()
                                    },
                                    secondary_action() {
                                        d.hide()
                                    }
                                })
                                d.$wrapper.find('.btn-link').css('width', '100px');
                                d.show()

                            
                        frm.set_value("number_of_sheets","")
                        frm.set_value("designation","")
                        frm.set_value("designation_2","")
                        frm.set_value("operators",[])
                        frm.set_value("helpers",[])
                        frm.refresh_fields("number_of_sheets")
                        // let i =0;
                        // for(let vl of frm.doc.raw_materials){
                        //     fields.push({'fieldtype':'Link', 'options':'Item', 'label':'Item', 'read_only':1, 'fieldname':`item${i}`, 'default':vl.item_code})
                        //     fields.push({'fieldtype':'Column Break'})
                        //     fields.push({'fieldtype':'Float', 'label':'Qty', 'fieldname':`qty${i}`})
                        //     fields.push({'fieldtype':'Column Break'})
                        //     fields.push({'fieldtype':'Time', 'label':'To Time', 'fieldname':`time${i}`})
                        //     fields.push({'fieldtype':'Section Break'})
                        //     i+=1;
                        // }

                        // frappe.prompt(fields, (values) => {
                        //     frm.events.complete_job(frm, "Complete", values);
                        //     console.log("========")
                        //     console.log(values)
                        //     // frm.events.complete_job(frm, "Complete", data.item_code0);
                        // },

                        //     __("Enter Value"));

                    }).addClass("btn-primary");

                }
            }


        }

        frm.fields_dict.laser_cutting.$wrapper[0].addEventListener("click", function () {
            if (frm.doc.laser_cutting.length == 1) {
                frm.fields_dict.laser_cutting.$wrapper.find('.grid-add-row')[0].style.display = 'none'
            }
        })
        if (frm.doc.laser_cutting.length == 1) {
            frm.fields_dict.laser_cutting.$wrapper.find('.grid-add-row')[0].style.display = 'none'
        }



        frm.set_query("item_code", "raw_materials", function () {
            return {
                query: "ohmgroups.ohm_groups.doctype.laser_cutting.laser_cutting.item_query",
                filters: {
                    "attribute_value": "Laser Cutting",
                }
            };
        });
        frm.set_query("item_code", "laser_cutting", function () {
            return {
                filters: {
                    item_group: "Sheet",

                },
            };
        });
    },
    reset_timer: function (frm) {
        frm.set_value('started_time', '');
    },
    // set:function(frm){
    //     frm.set_value("number_of_sheets","")
    //     frm.set_value("designation","")
    //     frm.set_value("designation_2","")
    //     frm.set_value("operators",[])
    //     frm.set_value("helpers",[])
    //     frm.refresh_fields("number_of_sheets")
    // },
    make_dashboard: function (frm) {
        if (frm.doc.__islocal)
            return;
        if (!frm.is_new() && frm.doc.docstatus == 0 && !(frm.doc.total_qty == frm.doc.total_completed_qty)) {
            frm.dashboard.refresh();
            const timer = `
                <div class="stopwatch" style="font-weight:bold;margin:0px 13px 0px 2px;
                    color:#545454;font-size:18px;display:inline-block;vertical-align:text-bottom;">
                    <span class="hours">00</span>
                    <span class="colon">:</span>
                    <span class="minutes">00</span>
                    <span class="colon">:</span>
                    <span class="seconds">00</span>
                </div>`;
            var section = frm.toolbar.page.add_inner_message(timer);
            let currentIncrement = frm.doc.current_time || 0;
            if (frm.doc.started_time || frm.doc.current_time) {
                if (frm.doc.status == "Draft") {
                    updateStopwatch(currentIncrement);
                } else {
                    currentIncrement += moment(frappe.datetime.now_datetime()).diff(moment(frm.doc.started_time), "seconds");
                    initialiseTimer();
                }

                function initialiseTimer() {
                    const interval = setInterval(function () {
                        var current = setCurrentIncrement();
                        updateStopwatch(current);
                    }, 1000);
                }

                function updateStopwatch(increment) {
                    var hours = Math.floor(increment / 3600);
                    var minutes = Math.floor((increment - (hours * 3600)) / 60);
                    var seconds = increment - (hours * 3600) - (minutes * 60);

                    $(section).find(".hours").text(hours < 10 ? ("0" + hours.toString()) : hours.toString());
                    $(section).find(".minutes").text(minutes < 10 ? ("0" + minutes.toString()) : minutes.toString());
                    $(section).find(".seconds").text(seconds < 10 ? ("0" + seconds.toString()) : seconds.toString());
                }

                function setCurrentIncrement() {
                    currentIncrement += 1;
                    return currentIncrement;
                }
            }
        }

    },
    validate: async function (frm) {
        frm.set_value("number_of_sheets","")
        frm.set_value("designation","")
        frm.set_value("designation_2","")
        frm.set_value("operators",[])
        frm.set_value("helpers",[])
        frm.refresh_fields("number_of_sheets")
        if ((!frm.doc.time_logs || !frm.doc.time_logs.length) && frm.doc.started_time) {
            frm.trigger("reset_timer");
        }
        if (frm.doc.frozen == 0) {
            let fields = []
            frappe.validated = false
            frappe.confirm("Are You Sure to send to Laser Cutting Work",
                function () {
                    frm.set_value("frozen", 1)
                    frm.save();
                    frappe.validated = true
                    if (frm.doc.frozen == 1) {
                        for (let i = 0; i < frappe.get_meta('Laser Cutting').fields.length; i++) {
                            if (frappe.get_meta('Laser Cutting').fields[i].fieldname == 'job_work_tab') { break; }
                            fields.push(frappe.get_meta('Laser Cutting').fields[i].fieldname)
                            frm.set_df_property(frappe.get_meta('Laser Cutting').fields[i].fieldname, 'read_only', 1)
                        }
                    }

                })
        }
        frm.call({
            method: "sheet_no",
            args: {
                laser_cutting: frm.doc.laser_cutting
            },
            callback: function (r) {
                // frm.reload_doc();
                frm.set_df_property('number_of_sheets', 'options', r.message)
            }
        });
        var dialog = new frappe.ui.Dialog({
            title: 'Are You Sure',
            primary_action_label: __('Yes'),
            primary_action: function (data) {
                cur_frm.set_value("frozen", 1)
            },
            secondary_action_label: __('No'),
            secondary_action: function (data) {
                frm.set_value("frozen", 1)
            }
        })
        if (!frm.doc.raw_materials) {
            frappe.msgprint("Kindly Upload the Raw Materials")
        }
        else if (frm.doc.raw_materials == 0) {
            frappe.msgprint("Kindly Upload the Raw Materials")
        }
        else {
            for (var i = 0; i < frm.doc.raw_materials.length; i++) {
                var rate = (await frappe.db.get_value('Item', { 'item_code': frm.doc.raw_materials[i].item_code }, 'valuation_rate')).message.valuation_rate
                frappe.model.set_value(frm.doc.raw_materials[i].doctype, frm.doc.raw_materials[i].name, 'basic_rate_as_per_stock_uom', rate)
                frappe.model.set_value(frm.doc.raw_materials[i].doctype, frm.doc.raw_materials[i].name, 'warehouse', "Stores - ONE")

            }
            frm.refresh()
        }
    },
    start_job: function (frm, status, employee) {
        const args = {
            oper: frm.doc.designation,
            help: frm.doc.designation_2,
            sheet: frm.doc.number_of_sheets,
            job_card_id: frm.doc.name,
            start_time: frappe.datetime.now_datetime(),
            employees: employee,
            status: status,

        };
        frm.events.make_time_log(frm, args);
    },

    complete_job: function (frm, status, table) {
        frm.set_value("number_of_sheets","")
        frm.set_value("designation","")
        frm.set_value("designation_2","")
        frm.set_value("operators",[])
        frm.set_value("helpers",[])
        frm.refresh_fields("number_of_sheets")
        const args = {
            complete_time: frappe.datetime.now_datetime(),
            job_card_id: frm.doc.name,
            status: status,
            table: table

        };
        frm.events.make_time_log(frm, args);
    },
    make_time_log: function (frm, args) {
        frm.set_value("number_of_sheets", "")
        frm.set_value("designation", "")
        frm.set_value("designation_2", "")
        frm.set_value("operators", [])
        frm.set_value("helpers", [])
        frm.events.update_sub_operation(frm, args);

        frm.call({
            method: "ohmgroups.ohm_groups.doctype.laser_cutting.laser_cutting.make_time_log",
            args: {
                args: args
            },
            freeze: true,
            callback: function () {
                frm.reload_doc();
                frm.trigger("make_dashboard");
            }
        });
    },
    update_sub_operation: function (frm, args) {
        if (frm.doc.sub_operations && frm.doc.sub_operations.length) {
            let sub_operations = frm.doc.sub_operations.filter(d => d.status != 'Complete');
            if (sub_operations && sub_operations.length) {
                args["sub_operation"] = sub_operations[0].sub_operation;
            }
        }
    },
    timer: function (frm) {
        return `<button> Start </button>`
    },
    designation: function (frm) {
        frm.set_query("operators", function () {
            return {
                filters: {
                    "designation": frm.doc.designation
                }

            }
        })
    },
    designation_2: function (frm) {
        frm.set_query("helpers", function () {
            return {
                filters: {
                    "designation": frm.doc.designation_2
                }

            }
        })
    }
});
frappe.ui.form.on('Laser Cutting Time Log', {
    to_time: function (frm) {
        frm.set_value('started_time', '');
    }
})

frappe.ui.form.on('Raw Materials', {
    raw_materials_add(frm, cdt, cdn) {
        // for(let i=0;i<frm.doc.raw_materials.length;i++){
        frappe.model.set_value(cdt, cdn, 'qty', frm.doc.laser_cutting ? frm.doc.laser_cutting[0].qty : 0)
        // }

    },
    item_code(frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        frappe.db.get_value('Item', { 'item_code': row.item_code }, 'valuation_rate').then((r) => {
            frappe.model.set_value(cdt, cdn, 'basic_rate_as_per_stock_uom', r.message.valuation_rate)
        })
    },
    per_sheet_qty(frm, cdt, cdn) {
        var row = locals[cdt][cdn]

        for (let i = 0; i < frm.doc.laser_cutting.length; i++) {
            frappe.model.set_value(cdt, cdn, 'total_qty', row.per_sheet_qty * frm.doc.laser_cutting[i].qty)
        }

    },
    qty(frm, cdt, cdn) {
        var row = locals[cdt][cdn]

        for (let i = 0; i < frm.doc.laser_cutting.length; i++) {
            frappe.model.set_value(cdt, cdn, 'total_qty', row.per_sheet_qty * row.qty)
        }
    },
})
frappe.ui.form.on('Finished Goods', {
    qty(frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        for (let i = 0; i < frm.doc.raw_materials.length; i++) {
            frappe.model.set_value(frm.doc.raw_materials[i].doctype, frm.doc.raw_materials[i].name, 'qty', row.qty)
        }

    },

})


