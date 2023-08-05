/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
//@ts-ignore
import style from "./elements.css";
import React from "react";
import { HiPlotLoadStatus, URL_LOAD_URI } from "./types";
import { RestoreDataBtn, ExcludeDataBtn, ExportDataCSVBtn, KeepDataBtn } from "./controls";
//@ts-ignore
import IconSVG from "../hiplot/static/icon.svg";
import { HiPlotTutorial } from "./tutorial/tutorial";
;
export class RunsSelectionTextArea extends React.Component {
    constructor(props) {
        super(props);
        this.container = React.createRef();
        this.textarea = React.createRef();
        this.state = {
            value: props.initialValue,
        };
    }
    onInput() {
        var elem = this.textarea.current;
        if (this.props.hasFocus || !this.props.minimizeWhenOutOfFocus) {
            elem.style.height = 'auto';
            elem.style.height = elem.scrollHeight + 'px';
            return;
        }
        elem.style.height = '25px';
    }
    onKeyDown(evt) {
        if (evt.which === 13 && !evt.shiftKey) {
            this.props.onSubmit(this.textarea.current.value);
            this.props.onFocusChange(false);
            evt.preventDefault();
        }
    }
    onFocusChange(evt) {
        if (evt.type == "focus") {
            this.props.onFocusChange(true);
        }
        else if (evt.type == "blur") {
            this.props.onFocusChange(false);
        }
    }
    componentDidMount() {
        this.onInput();
    }
    componentDidUpdate() {
        this.onInput();
    }
    render() {
        return (React.createElement("div", { ref: this.container, className: this.props.hasFocus || !this.props.minimizeWhenOutOfFocus ? " col-md-11" : " col-md-3" },
            React.createElement("textarea", { ref: this.textarea, className: style.runsSelectionTextarea, disabled: !this.props.enabled, value: this.state.value, onKeyDown: this.onKeyDown.bind(this), onInput: this.onInput.bind(this), onChange: (evt) => this.setState({ value: evt.target.value }), onFocus: this.onFocusChange.bind(this), onBlur: this.onFocusChange.bind(this), placeholder: "Experiments to load" })));
    }
}
;
;
export class HeaderBar extends React.Component {
    constructor(props) {
        super(props);
        this.selected_count_ref = React.createRef();
        this.selected_pct_ref = React.createRef();
        this.total_count_ref = React.createRef();
        this.controls_root_ref = React.createRef();
        this.state = {
            isTextareaFocused: false,
            hasTutorial: false,
        };
    }
    recomputeMetrics() {
        if (!this.selected_count_ref.current) {
            return;
        }
        const selected_count = this.props.rows.selected.get().length;
        const total_count = this.props.rows.all.get().length;
        this.selected_count_ref.current.innerText = '' + selected_count;
        this.selected_pct_ref.current.innerText = '' + (100 * selected_count / total_count).toPrecision(3);
        this.total_count_ref.current.innerText = '' + total_count;
    }
    componentDidMount() {
        this.props.rows.selected.on_change(function (rows) {
            this.recomputeMetrics();
        }.bind(this), this);
        this.props.rows.all.on_change(function (rows) {
            this.recomputeMetrics();
        }.bind(this), this);
        this.recomputeMetrics();
    }
    componentWillUnmount() {
        this.props.rows.off(this);
    }
    componentDidUpdate() {
        this.recomputeMetrics();
    }
    onToggleTutorial() {
        this.setState(function (prevState, prevProps) {
            return {
                hasTutorial: !prevState.hasTutorial
            };
        });
    }
    renderControls() {
        const hasTextArea = this.props.onRequestLoadExperiment != null;
        return (React.createElement(React.Fragment, null,
            hasTextArea &&
                React.createElement(RunsSelectionTextArea, { initialValue: this.props.url_state.get(URL_LOAD_URI, ''), enabled: this.props.loadStatus != HiPlotLoadStatus.Loading, minimizeWhenOutOfFocus: this.props.loadStatus == HiPlotLoadStatus.Loaded, onSubmit: this.props.onRequestLoadExperiment, onFocusChange: (hasFocus) => this.setState({ isTextareaFocused: hasFocus }), hasFocus: this.state.isTextareaFocused }),
            this.props.loadStatus == HiPlotLoadStatus.Loaded && !this.state.isTextareaFocused &&
                React.createElement(React.Fragment, null,
                    React.createElement("div", { className: "col-md-5" },
                        React.createElement(RestoreDataBtn, { rows: this.props.rows }),
                        React.createElement(KeepDataBtn, { rows: this.props.rows }),
                        React.createElement(ExcludeDataBtn, { rows: this.props.rows }),
                        this.props.onRequestRefreshExperiment != null &&
                            React.createElement("button", { title: "Refresh + restore data removed", onClick: this.props.onRequestRefreshExperiment }, "Refresh"),
                        React.createElement(ExportDataCSVBtn, { rows: this.props.rows }),
                        React.createElement("button", { title: "Start HiPlot tutorial", onClick: this.onToggleTutorial.bind(this) }, "Help"),
                        React.createElement("div", { style: { clear: 'both' } })),
                    React.createElement("div", { className: hasTextArea ? "col-md-3" : "col-md-6" },
                        React.createElement("div", { style: { "fontFamily": "monospace" } },
                            "Selected: ",
                            React.createElement("strong", { ref: this.selected_count_ref, style: { "minWidth": "4em", "textAlign": "right", "display": "inline-block" } }, "??"),
                            "/",
                            React.createElement("strong", { ref: this.total_count_ref, style: { "minWidth": "4em", "textAlign": "left", "display": "inline-block" } }, "??"),
                            " (",
                            React.createElement("span", { ref: this.selected_pct_ref }, "??"),
                            "%)")))));
    }
    render() {
        var controlsOrTutorial = this.state.hasTutorial ?
            (React.createElement("div", { className: "col-md-11" },
                React.createElement(HiPlotTutorial, { navbarRoot: this.controls_root_ref, onTutorialDone: (() => this.setState({ hasTutorial: false })).bind(this) }))) :
            this.renderControls();
        return (React.createElement("div", { ref: this.controls_root_ref, className: "container-fluid " + style.header },
            React.createElement("div", { className: "form-row" },
                React.createElement("div", { className: "col-md-1" },
                    React.createElement("img", { style: { height: '55px' }, src: IconSVG })),
                controlsOrTutorial)));
    }
}
;
export class ErrorDisplay extends React.Component {
    render() {
        return (React.createElement("div", { className: "alert alert-danger", role: "alert" },
            React.createElement("div", { className: "container" },
                React.createElement("h4", { className: "alert-heading" }, this.props.error),
                React.createElement("p", { className: "mb-0" }, "The error above was returned by the server when trying to load your experiment"))));
    }
}
