import React from "react";
import './global';
import { Datapoint, HiPlotExperiment, HiPlotLoadStatus } from "./types";
import { RowsDisplayTable } from "./rowsdisplaytable";
import { HiPlotPluginData } from "./plugin";
export { PlotXY } from "./plotxy";
export { ParallelPlot } from "./parallel";
export { RowsDisplayTable } from "./rowsdisplaytable";
export { HiPlotPluginData } from "./plugin";
export { Datapoint, HiPlotExperiment, AllDatasets, HiPlotLoadStatus } from "./types";
interface PluginInfo {
    name: string;
    render: (plugin_data: HiPlotPluginData) => JSX.Element;
}
interface HiPlotComponentProps {
    experiment: HiPlotExperiment | null;
    is_webserver: boolean;
    plugins: Array<PluginInfo>;
}
interface HiPlotComponentState {
    experiment: HiPlotExperiment | null;
    version: number;
    loadStatus: HiPlotLoadStatus;
    error: string;
}
export declare class HiPlotComponent extends React.Component<HiPlotComponentProps, HiPlotComponentState> {
    domRoot: React.RefObject<HTMLDivElement>;
    comm: any;
    comm_selection_id: number;
    table: RowsDisplayTable;
    data: HiPlotPluginData;
    constructor(props: HiPlotComponentProps);
    static defaultProps: {
        is_webserver: boolean;
    };
    onSelectedChange(selection: Array<Datapoint>): void;
    recomputeParamsDef(all_data: Array<Datapoint>): void;
    _loadExperiment(experiment: HiPlotExperiment): void;
    loadWithPromise(prom: Promise<any>): void;
    setup_comm(comm_: any): void;
    componentWillUnmount(): void;
    componentDidMount(): void;
    componentDidUpdate(): void;
    columnContextMenu(column: string, cm: HTMLDivElement): void;
    onRefreshDataBtn(): void;
    loadURI(uri: string): void;
    onRunsTextareaSubmitted(uri: string): void;
    render(): JSX.Element;
}
export declare function hiplot_setup(element: HTMLElement, extra?: object): void;
