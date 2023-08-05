/// <reference types="jquery" />
/// <reference types="datatables.net" />
/// <reference types="bootstrap" />
import React from "react";
import { Datapoint } from "./types";
import { HiPlotPluginData } from "./plugin";
interface RowsDisplayTableState {
}
export declare class RowsDisplayTable extends React.Component<HiPlotPluginData, RowsDisplayTableState> {
    table_ref: React.RefObject<HTMLTableElement>;
    dt: any;
    dom: JQuery;
    ordered_cols: Array<string>;
    empty: boolean;
    constructor(props: HiPlotPluginData);
    componentDidMount(): void;
    set_selected(selected: Array<Datapoint>): void;
    render(): JSX.Element;
    componentWillUnmount(): void;
}
export {};
