import React from "react";
import * as d3 from "d3";
import { WatchedProperty, AllDatasets } from "./types";
import { ParamDefMap } from "./infertypes";
import { HiPlotPluginData } from "./plugin";
export interface ParallelPlotInternalState {
    colorby: WatchedProperty;
    rows: AllDatasets;
    params_def: ParamDefMap;
}
export interface StringMapping<V> {
    [key: string]: V;
}
interface ParallelPlotState {
    height: number;
    width: number;
    order: Array<string>;
    hide: Set<string>;
    invert: Set<string>;
}
interface ParallelPlotData extends HiPlotPluginData {
    order?: Array<string>;
    hide?: Set<string>;
    invert?: Set<string>;
    data: any;
}
export declare class ParallelPlot extends React.Component<ParallelPlotData, ParallelPlotState> {
    on_resize: () => void;
    on_unmount: Array<() => void>;
    m: number[];
    w: number;
    h: number;
    xscale: any;
    debounced_brush: any;
    root_ref: React.RefObject<HTMLDivElement>;
    foreground_ref: React.RefObject<HTMLCanvasElement>;
    foreground: CanvasRenderingContext2D;
    background_ref: React.RefObject<HTMLCanvasElement>;
    background: CanvasRenderingContext2D;
    highlighted_ref: React.RefObject<HTMLCanvasElement>;
    highlighted: CanvasRenderingContext2D;
    svg: any;
    svgg: any;
    div: any;
    dimensions: Array<string>;
    yscale: StringMapping<any>;
    axis: any;
    d3brush: d3.BrushBehavior<unknown>;
    constructor(props: ParallelPlotData);
    static defaultProps: {
        data: {};
    };
    componentWillUnmount(): void;
    componentDidUpdate(prevProps: any, prevState: any): void;
    onResizeH(height: number): void;
    onWindowResize: any;
    render(): JSX.Element;
    componentDidMount(): void;
    setScaleRange(k: string): void;
    createScale(k: string): any;
    compute_dimensions(): void;
}
export {};
