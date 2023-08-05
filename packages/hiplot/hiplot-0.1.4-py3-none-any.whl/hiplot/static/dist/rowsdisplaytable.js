/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import $ from "jquery";
import React from "react";
//@ts-ignore
import dt from "datatables.net-bs4";
dt(window, $);
//@ts-ignore
import dtReorder from "datatables.net-colreorder-bs4";
dtReorder(window, $);
//@ts-ignore
import style from "./hiplot.css";
;
export class RowsDisplayTable extends React.Component {
    constructor(props) {
        super(props);
        this.table_ref = React.createRef();
        this.dt = null;
        this.ordered_cols = [];
        this.state = {};
    }
    componentDidMount() {
        this.dom = $(this.table_ref.current);
        this.ordered_cols = ['uid'];
        var me = this;
        $.each(this.props.params_def, function (k, def) {
            if (k == me.ordered_cols[0]) {
                return;
            }
            me.ordered_cols.push(k);
        });
        this.dom.empty();
        this.dt = this.dom.DataTable({
            columns: this.ordered_cols.map(function (x) {
                if (x == "uid") {
                    return {
                        'title': x,
                        'defaultContent': 'null',
                        'createdCell': function (td, row_uid, rowData, row, col) {
                            var color = me.props.get_color_for_row(me.props.dp_lookup[row_uid], 1.0);
                            $(td).prepend($('<span>').addClass('color-block').css('background-color', color));
                        }
                    };
                }
                return {
                    'title': x,
                    'defaultContent': 'null'
                };
            }),
            data: [],
            deferRender: true,
            //@ts-ignore
            colReorder: true,
            buttons: ['csv'],
        });
        this.empty = true;
        this.dom.find('tbody')
            .on('mouseenter', 'td', function () {
            if (!me.dt || me.empty) {
                return;
            }
            var rowIdx = me.dt.cell(this).index().row;
            var row = me.dt.row(rowIdx);
            var individualUidColIdx = me.dt.colReorder.order().indexOf(0);
            $(me.dt.cells().nodes()).removeClass(style.highlight);
            $(row.nodes()).addClass(style.highlight);
            me.props.rows['highlighted'].set([me.props.dp_lookup[row.data()[individualUidColIdx]]]);
        })
            .on("mouseout", "td", function () {
            if (!me.dt || me.empty) {
                return;
            }
            var rowIdx = me.dt.cell(this).index().row;
            $(me.dt.row(rowIdx).nodes()).removeClass(style.highlight);
            me.props.rows['highlighted'].set([]);
        });
        me.set_selected(me.props.rows['selected'].get());
        me.props.rows['selected'].on_change(function (selection) {
            me.set_selected(selection);
        }, this);
    }
    set_selected(selected) {
        var dt = this.dt;
        var ordered_cols = this.ordered_cols;
        dt.clear();
        dt.rows.add(selected.map(function (row) {
            return dt.colReorder.transpose([...Array(ordered_cols.length).keys()]).map(x => row[ordered_cols[x]]);
        }));
        dt.draw();
        this.empty = selected.length == 0;
    }
    render() {
        return (React.createElement("div", { className: `${style.wrap} container-fluid` },
            React.createElement("div", { className: "row" },
                React.createElement("div", { className: `col-md-12 sample-table-container` },
                    React.createElement("table", { ref: this.table_ref, className: "sample-rows-table display table table-striped table-bordered dataTable" })))));
    }
    componentWillUnmount() {
        if (this.dt) {
            this.dt.destroy();
        }
        this.props.rows.off(this);
    }
}
