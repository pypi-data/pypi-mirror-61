/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";
//@ts-ignore
import JSON5 from "json5";
import './global';
import { WatchedProperty, ParamType, AllDatasets, HiPlotLoadStatus, URL_COLOR_BY, URL_LOAD_URI } from "./types";
import { RowsDisplayTable } from "./rowsdisplaytable";
import { infertypes } from "./infertypes";
import { PageState } from "./lib/savedstate";
import { ParallelPlot } from "./parallel";
import { PlotXY } from "./plotxy";
import { SelectedCountProgressBar } from "./controls";
import { ErrorDisplay, HeaderBar } from "./elements";
//@ts-ignore
import LogoSVG from "../hiplot/static/logo.svg";
//@ts-ignore
import style from "./hiplot.css";
import { ContextMenu } from "./contextmenu";
// Exported from HiPlot
export { PlotXY } from "./plotxy";
export { ParallelPlot } from "./parallel";
export { RowsDisplayTable } from "./rowsdisplaytable";
export { AllDatasets, HiPlotLoadStatus } from "./types";
;
;
function make_hiplot_data() {
    return {
        params_def: {},
        rows: new AllDatasets(),
        get_color_for_row: null,
        render_row_text: function (row) {
            return row.uid;
        },
        dp_lookup: {},
        context_menu_ref: React.createRef(),
        colorby: new WatchedProperty('colorby'),
        experiment: null,
        url_state: PageState.create_state('hip'),
    };
}
export class HiPlotComponent extends React.Component {
    constructor(props) {
        super(props);
        // React refs
        this.domRoot = React.createRef();
        this.comm = null;
        this.comm_selection_id = 0;
        this.table = null;
        this.data = make_hiplot_data();
        this.state = {
            experiment: props.experiment,
            version: 0,
            loadStatus: HiPlotLoadStatus.None,
            error: null,
        };
        var rows = this.data.rows;
        rows['selected'].on_change(this.onSelectedChange.bind(this), this);
        rows['all'].on_change(this.recomputeParamsDef.bind(this), this);
    }
    onSelectedChange(selection) {
        this.comm_selection_id += 1;
        if (this.comm !== null) {
            this.comm.send({
                'type': 'selection',
                'selection_id': this.comm_selection_id,
                'selected': selection.map(row => '' + row['uid'])
            });
        }
    }
    recomputeParamsDef(all_data) {
        Object.assign(this.data.params_def, infertypes(this.data.url_state.children('params'), all_data, this.data.params_def));
    }
    _loadExperiment(experiment) {
        //console.log('Load xp', experiment);
        var me = this;
        me.data.experiment = experiment;
        var rows = this.data.rows;
        // Generate dataset for Parallel Plot
        me.data.dp_lookup = {};
        rows['experiment_all'].set(experiment.datapoints.map(function (t) {
            var csv_obj = $.extend({
                "uid": t.uid,
                "from_uid": t.from_uid,
            }, t.values);
            me.data.dp_lookup[t.uid] = csv_obj;
            return csv_obj;
        }));
        rows['all'].set(rows['experiment_all'].get());
        rows['selected'].set(rows['experiment_all'].get());
        me.data.params_def = infertypes(this.data.url_state.children('params'), rows['all'].get(), experiment.parameters_definition);
        // Color handling
        function get_default_color() {
            function select_as_coloring_score(r) {
                var pd = me.data.params_def[r];
                var score = 0;
                if (pd.colors !== null) {
                    score += 100;
                }
                if (pd.type == ParamType.CATEGORICAL) {
                    score -= 20;
                }
                if (pd.optional) {
                    score -= 40;
                }
                return score;
            }
            ;
            var possibles = Object.keys(me.data.params_def).sort((a, b) => select_as_coloring_score(b) - select_as_coloring_score(a));
            return possibles[0];
        }
        this.data.colorby.set(this.data.url_state.get(URL_COLOR_BY, get_default_color()));
        if (me.data.params_def[this.data.colorby.get()] === undefined) {
            this.data.colorby.set(get_default_color());
        }
        this.data.colorby.on_change(function (f) {
            me.data.url_state.set(URL_COLOR_BY, f);
        }, this);
        this.data.get_color_for_row = function (trial, alpha) {
            return me.data.params_def[me.data.colorby.get()].colorScheme(trial[me.data.colorby.get()], alpha);
        };
    }
    loadWithPromise(prom) {
        var me = this;
        me.setState({ loadStatus: HiPlotLoadStatus.Loading });
        prom.then(function (data) {
            if (data.experiment === undefined) {
                console.log("Experiment loading failed", data);
                me.setState({
                    loadStatus: HiPlotLoadStatus.Error,
                    experiment: null,
                    error: data.error !== undefined ? data.error : 'Unable to load experiment',
                });
                return;
            }
            me._loadExperiment(data.experiment);
            me.setState(function (state, props) {
                return {
                    experiment: data.experiment,
                    version: state.version + 1,
                    loadStatus: HiPlotLoadStatus.Loaded,
                };
            });
        })
            .catch(error => {
            console.log('Error', error);
            me.setState({ loadStatus: HiPlotLoadStatus.Error, experiment: null, error: 'HTTP error, check server logs / javascript console' });
            throw error;
        });
    }
    setup_comm(comm_) {
        this.comm = comm_;
        console.log("Setting up communication channel", comm_);
        this.onSelectedChange(this.data.rows['selected'].get());
    }
    componentWillUnmount() {
        this.data.context_menu_ref.current.removeCallbacks(this);
        this.data.rows.off(this);
        this.data.colorby.off(this);
    }
    componentDidMount() {
        // Setup contextmenu when we right-click a parameter
        var me = this;
        me.data.context_menu_ref.current.addCallback(this.columnContextMenu.bind(this), this);
        // Load experiment provided in constructor if any
        if (this.props.experiment !== null) {
            this.loadWithPromise(new Promise(function (resolve, reject) {
                resolve({ experiment: this.props.experiment });
            }.bind(this)));
        }
        else {
            var load_uri = this.data.url_state.get(URL_LOAD_URI);
            if (load_uri !== undefined) {
                this.loadURI(load_uri);
            }
        }
    }
    componentDidUpdate() {
        if (this.state.loadStatus == HiPlotLoadStatus.None) {
            this.data = make_hiplot_data();
        }
    }
    columnContextMenu(column, cm) {
        const VAR_TYPE_TO_NAME = {
            [ParamType.CATEGORICAL]: 'Categorical',
            [ParamType.NUMERIC]: 'Number',
            [ParamType.NUMERICLOG]: 'Number (log-scale)',
            [ParamType.NUMERICPERCENTILE]: 'Number (percentile-scale)',
        };
        var contextmenu = $(cm);
        contextmenu.append($('<h6 class="dropdown-header">Data scaling</h6>'));
        this.data.params_def[column].type_options.forEach(function (possible_type) {
            var option = $('<a class="dropdown-item" href="#">').text(VAR_TYPE_TO_NAME[possible_type]);
            if (possible_type == this.data.params_def[column].type) {
                option.addClass('disabled').css('pointer-events', 'none');
            }
            option.click(function (event) {
                contextmenu.css('display', 'none');
                this.data.params_def[column].type = possible_type;
                this.data.params_def[column].__url_state__.set('type', possible_type);
                this.data.rows['all'].append([]); // Trigger recomputation of the parameters + rerendering
                event.preventDefault();
            }.bind(this));
            contextmenu.append(option);
        }.bind(this));
        contextmenu.append($('<div class="dropdown-divider"></div>'));
        // Color by
        var link_colorize = $('<a class="dropdown-item" href="#">Use for coloring</a>');
        link_colorize.click(function (event) {
            this.data.colorby.set(column);
            event.preventDefault();
        }.bind(this));
        if (this.data.colorby.get() == column) {
            link_colorize.addClass('disabled').css('pointer-events', 'none');
        }
        contextmenu.append(link_colorize);
    }
    onRefreshDataBtn() {
        this.loadURI(this.data.url_state.get(URL_LOAD_URI));
    }
    loadURI(uri) {
        this.loadWithPromise(new Promise(function (resolve, reject) {
            $.get("/data?uri=" + encodeURIComponent(uri), resolve, "json").fail(function (data) {
                //console.log("Data loading failed", data);
                if (data.readyState == 4 && data.status == 200) {
                    console.log('Unable to parse JSON with JS default decoder (Maybe it contains NaNs?). Trying custom decoder');
                    var decoded = JSON5.parse(data.responseText);
                    resolve(decoded);
                }
                else if (data.status == 0) {
                    resolve({
                        'experiment': undefined,
                        'error': 'Network error'
                    });
                    return;
                }
                else {
                    reject(data);
                }
            });
        }));
    }
    onRunsTextareaSubmitted(uri) {
        this.data.url_state.clear();
        this.data.url_state.set(URL_LOAD_URI, uri);
        this.loadURI(uri);
    }
    render() {
        return (React.createElement("div", { className: "scoped_css_bootstrap" },
            React.createElement("div", { ref: this.domRoot, className: style.hiplot },
                React.createElement(SelectedCountProgressBar, { rows: this.data.rows }),
                React.createElement(HeaderBar, Object.assign({ onRequestLoadExperiment: this.props.is_webserver ? this.onRunsTextareaSubmitted.bind(this) : null, onRequestRefreshExperiment: this.props.is_webserver ? this.onRefreshDataBtn.bind(this) : null, loadStatus: this.state.loadStatus }, this.data)),
                this.state.loadStatus == HiPlotLoadStatus.Error &&
                    React.createElement(ErrorDisplay, { error: this.state.error }),
                this.state.loadStatus != HiPlotLoadStatus.Loaded &&
                    React.createElement(DocAndCredits, null),
                React.createElement(ContextMenu, { ref: this.data.context_menu_ref }),
                this.state.loadStatus == HiPlotLoadStatus.Loaded &&
                    React.createElement("div", null, this.props.plugins.map((plugin_info, idx) => React.createElement(React.Fragment, { key: idx }, plugin_info.render({
                        ...this.data,
                        ...(this.state.experiment._displays[plugin_info.name] ? this.state.experiment._displays[plugin_info.name] : {}),
                        url_state: this.data.url_state.children(plugin_info.name)
                    })))))));
    }
}
HiPlotComponent.defaultProps = {
    is_webserver: false,
};
class DocAndCredits extends React.Component {
    render() {
        return (React.createElement("div", { className: "container hide-when-loaded" },
            React.createElement("div", { className: "row" },
                React.createElement("div", { className: "col-md-3" }),
                React.createElement("div", { className: "col-md-6" },
                    React.createElement("img", { src: LogoSVG })),
                React.createElement("div", { className: "col-md-3" }),
                React.createElement("div", { className: "col-md-6" },
                    React.createElement("h3", null, "Controls"),
                    React.createElement("p", null,
                        React.createElement("strong", null, "Brush"),
                        ": Drag vertically along an axis.",
                        React.createElement("br", null),
                        React.createElement("strong", null, "Remove Brush"),
                        ": Tap the axis background.",
                        React.createElement("br", null),
                        React.createElement("strong", null, "Reorder Axes"),
                        ": Drag a label horizontally.",
                        React.createElement("br", null),
                        React.createElement("strong", null, "Invert Axis"),
                        ": Tap an axis label.",
                        React.createElement("br", null),
                        React.createElement("strong", null, "Remove Axis"),
                        ": Drag axis label to the left edge.",
                        React.createElement("br", null))),
                React.createElement("div", { className: "cold-md-6" },
                    React.createElement("h3", null, "Credits & License"),
                    React.createElement("p", null,
                        "Adapted from examples by",
                        React.createElement("br", null),
                        React.createElement("a", { href: "http://bl.ocks.org/syntagmatic/3150059" }, "Kai"),
                        ", ",
                        React.createElement("a", { href: "http://bl.ocks.org/1341021" }, "Mike Bostock"),
                        " and ",
                        React.createElement("a", { href: "http://bl.ocks.org/1341281" }, "Jason Davies"),
                        React.createElement("br", null)),
                    React.createElement("p", null,
                        "Released under the ",
                        React.createElement("strong", null, "MIT License"),
                        ".")))));
    }
}
;
export function hiplot_setup(element, extra) {
    var xydata = {};
    var pplotdata = {};
    var props = {
        experiment: null,
        is_webserver: true,
        plugins: [
            // Names correspond to values of hip.Displays
            { name: "PARALLEL_PLOT", render: (plugin_data) => React.createElement(ParallelPlot, Object.assign({ data: pplotdata }, plugin_data)) },
            { name: "XY", render: (plugin_data) => React.createElement(PlotXY, Object.assign({ name: "XY", data: xydata }, plugin_data)) },
            { name: "TABLE", render: (plugin_data) => React.createElement(RowsDisplayTable, Object.assign({}, plugin_data)) },
        ]
    };
    if (extra !== undefined) {
        Object.assign(props, extra);
    }
    return ReactDOM.render(React.createElement(HiPlotComponent, Object.assign({}, props)), element);
}
Object.assign(window, {
    'hiplot_setup': hiplot_setup,
});
