/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
;
;
export class WatchedProperty {
    constructor(name) {
        this.name = name;
        this.__on_change_handlers = [];
        this.value = undefined;
    }
    set(value) {
        this.value = value;
        this.__on_change_handlers.forEach(function (trigger) {
            trigger.cb(value);
        });
    }
    get() {
        return this.value;
    }
    on_change(cb, obj) {
        this.__on_change_handlers.push({ cb: cb, obj: obj });
    }
    off(obj) {
        this.__on_change_handlers = this.__on_change_handlers.filter(trigger => trigger.obj != obj);
    }
}
export class Dataset {
    constructor(name) {
        this.name = name;
        this.rows = [];
        this.on_change_fn = [];
        this.on_append_fn = [];
        this.named_childs = {};
    }
    set(new_rows) {
        this._set(new_rows);
    }
    append(new_rows) {
        this._append(new_rows);
    }
    _set(new_rows) {
        var rows = this.rows = new_rows;
        this.on_change_fn.forEach(function (trigger) {
            trigger.cb(rows);
        });
        Object.entries(this.named_childs).forEach(function (val) {
            val[1]._set(new_rows);
        });
    }
    _append(new_rows) {
        var rows = this.rows = this.rows.concat(new_rows);
        this.on_change_fn.forEach(function (trigger) {
            trigger.cb(rows);
        });
        this.on_append_fn.forEach(function (trigger) {
            trigger.cb(new_rows);
        });
        Object.entries(this.named_childs).forEach(function (val) {
            val[1]._append(new_rows);
        });
    }
    get() {
        return this.rows;
    }
    on_change(cb, obj) {
        this.on_change_fn.push({ cb: cb, obj: obj });
    }
    on_append(cb, obj) {
        this.on_append_fn.push({ cb: cb, obj: obj });
    }
    off(obj) {
        this.on_change_fn = this.on_change_fn.filter(function (value) {
            return value.obj != obj;
        });
        this.on_append_fn = this.on_append_fn.filter(function (value) {
            return value.obj != obj;
        });
    }
}
export class AllDatasets {
    constructor(experiment_all = new Dataset("experiment_all"), all = new Dataset("all"), // Everything after filtering
    selected = new Dataset("selected"), // What we currently select (with parallel plot)
    rendered = new Dataset("rendered"), // What we have rendered on the screen
    highlighted = new Dataset("highlighted")) {
        this.experiment_all = experiment_all;
        this.all = all;
        this.selected = selected;
        this.rendered = rendered;
        this.highlighted = highlighted;
    }
    off(obj) {
        this.experiment_all.off(obj);
        this.all.off(obj);
        this.selected.off(obj);
        this.rendered.off(obj);
        this.highlighted.off(obj);
    }
}
export var ParamType;
(function (ParamType) {
    ParamType["CATEGORICAL"] = "categorical";
    ParamType["NUMERIC"] = "numeric";
    ParamType["NUMERICLOG"] = "numericlog";
    ParamType["NUMERICPERCENTILE"] = "numericpercentile";
})(ParamType || (ParamType = {}));
;
;
export var HiPlotLoadStatus;
(function (HiPlotLoadStatus) {
    HiPlotLoadStatus[HiPlotLoadStatus["None"] = 0] = "None";
    HiPlotLoadStatus[HiPlotLoadStatus["Loading"] = 1] = "Loading";
    HiPlotLoadStatus[HiPlotLoadStatus["Loaded"] = 2] = "Loaded";
    HiPlotLoadStatus[HiPlotLoadStatus["Error"] = 3] = "Error";
})(HiPlotLoadStatus || (HiPlotLoadStatus = {}));
;
export const URL_LOAD_URI = 'load_uri';
export const URL_COLOR_BY = 'color_by';
