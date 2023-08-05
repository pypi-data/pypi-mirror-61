/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import $ from "jquery";
import React from "react";
//@ts-ignore
import style from "./tutorial.css";
;
class StepParallelPlot extends React.Component {
    componentDidMount() {
        $(this.props.rootRef.current.parentElement).find('.pplot-root').addClass(style.highlightElement);
    }
    componentWillUnmount() {
        $(this.props.rootRef.current.parentElement).find('.pplot-root').removeClass(style.highlightElement);
    }
    render() {
        return (React.createElement("div", { className: "alert alert-info", role: "alert" },
            React.createElement("h4", { className: "alert-heading" }, "Step 1/4: The parallel plot"),
            React.createElement("p", null,
                "The first plot you see above is a ",
                React.createElement("strong", null, "Parallel Plot"),
                ". Parallel plots are a convenient way to visualize and filter high-dimensional data. HiPlot will draw one vertical scaled axis for each metric you have in your dataset, and each training/data point is a continuous line that goes through its value on each of the axes."),
            React.createElement("hr", null),
            React.createElement("p", { className: "mb-0" },
                "Learn more about ",
                React.createElement("a", { href: "https://en.wikipedia.org/wiki/Parallel_coordinates" }, "Parallel coordinates"),
                " on Wikipedia.")));
    }
}
class StepLearnToSlice extends React.Component {
    componentDidMount() {
        $(this.props.rootRef.current.parentElement).find('.pplot-brush').addClass(style.highlightElement);
    }
    componentWillUnmount() {
        $(this.props.rootRef.current.parentElement).find('.pplot-brush').removeClass(style.highlightElement);
    }
    render() {
        return (React.createElement("div", { className: "alert alert-info", role: "alert" },
            React.createElement("h4", { className: "alert-heading" }, "Step 2/4: Slicing data"),
            React.createElement("p", null,
                "Slicing along an axis allows to discover patterns in the data. ",
                React.createElement("strong", null, "Drag vertically along an axis"),
                " to display only a subset of the data. You also can do it on several axis at the same time."),
            React.createElement("hr", null),
            React.createElement("p", { className: "mb-0" }, "To remove a slicing on an axis, click on the axis.")));
    }
}
class StepMoveAndRemoveColumns extends React.Component {
    componentDidMount() {
        $(this.props.rootRef.current.parentElement).find('.pplot-label').addClass(style.highlightText);
    }
    componentWillUnmount() {
        $(this.props.rootRef.current.parentElement).find('.pplot-label').removeClass(style.highlightText);
    }
    render() {
        return (React.createElement("div", { className: "alert alert-info", role: "alert" },
            React.createElement("h4", { className: "alert-heading" }, "Step 3/4: Move and remove axis"),
            React.createElement("p", null,
                "Move an axis by ",
                React.createElement("strong", null, "dragging its label above"),
                ". In parallel plots, we can very easily spot relationships between nearby axis. You can also ",
                React.createElement("strong", null, "remove"),
                " an axis by moving it all the way to the left or to the right.")));
    }
}
class StepDataTypeAndScaling extends React.Component {
    componentDidMount() {
        $(this.props.rootRef.current.parentElement).find('.pplot-label').addClass(style.highlightText);
    }
    componentWillUnmount() {
        $(this.props.rootRef.current.parentElement).find('.pplot-label').removeClass(style.highlightText);
    }
    render() {
        return (React.createElement("div", { className: "alert alert-info", role: "alert" },
            React.createElement("h4", { className: "alert-heading" }, "Step 4/4: Data type and scaling"),
            React.createElement("p", null,
                React.createElement("strong", null, "Right click on an axis"),
                " to see options. You can chose how to color your datapoints, change the scaling and more!"),
            React.createElement("hr", null),
            React.createElement("p", { className: "mb-0" },
                "In this same menu, you can enable an ",
                React.createElement("strong", null, "XY plot"),
                " by selecting an X and Y axis.")));
    }
}
class StepTutorialDone extends React.Component {
    render() {
        return (React.createElement("div", { className: "alert alert-success", role: "alert" },
            React.createElement("h4", { className: "alert-heading" }, "Well done!"),
            React.createElement("p", null,
                "Aww yeah, you successfully finished the tutorial! We hope you enjoy using HiPlot :)",
                React.createElement("br", null),
                React.createElement("a", { href: "https://facebookresearch.github.io/hiplot/" }, "Check the documentation"),
                " to learn more, or click ",
                React.createElement("strong", null, "Done"),
                " to finish the tutorial."),
            React.createElement("hr", null),
            React.createElement("p", { className: "mb-0" }, "Did you know that you can use HiPlot in your ipython notebooks as well?")));
    }
}
;
;
export class HiPlotTutorial extends React.Component {
    constructor(props) {
        super(props);
        this.steps = [
            (p) => React.createElement(StepParallelPlot, Object.assign({}, p)),
            (p) => React.createElement(StepLearnToSlice, Object.assign({}, p)),
            (p) => React.createElement(StepMoveAndRemoveColumns, Object.assign({}, p)),
            (p) => React.createElement(StepDataTypeAndScaling, Object.assign({}, p)),
            (p) => React.createElement(StepTutorialDone, Object.assign({}, p)),
        ];
        this.state = {
            stepNum: 0
        };
    }
    onClickNextTutorial() {
        this.setState(function (prevState, prevProps) {
            return {
                stepNum: Math.min(prevState.stepNum + 1, this.steps.length - 1)
            };
        });
    }
    onClickPreviousTutorial() {
        this.setState(function (prevState, prevProps) {
            return {
                stepNum: Math.max(prevState.stepNum - 1, 0)
            };
        });
    }
    render() {
        return (React.createElement("div", { className: `row ${style.tutoAlert}` },
            React.createElement("div", { className: "col-md-9" }, this.steps[this.state.stepNum]({
                rootRef: this.props.navbarRoot
            })),
            React.createElement("div", { className: "col-md-3" },
                this.state.stepNum > 0 && React.createElement("button", { className: "btn btn-outline-primary", onClick: this.onClickPreviousTutorial.bind(this) }, "Previous"),
                this.state.stepNum + 1 < this.steps.length &&
                    React.createElement("button", { className: "btn btn-outline-primary", onClick: this.onClickNextTutorial.bind(this) }, "Next"),
                this.state.stepNum + 1 == this.steps.length &&
                    React.createElement("button", { className: "btn btn-outline-primary", onClick: () => this.props.onTutorialDone() }, "Done"))));
    }
}
