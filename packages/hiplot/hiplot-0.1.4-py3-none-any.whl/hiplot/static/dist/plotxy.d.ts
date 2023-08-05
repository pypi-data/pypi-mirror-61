import { WatchedProperty } from "./types";
import { ParamDefMap } from "./infertypes";
import { HiPlotPluginData } from "./plugin";
import React from "react";
interface PlotXYProps extends HiPlotPluginData {
    name: string;
    data: any;
}
interface PlotXYState {
    width: number;
    height: number;
    enabled: boolean;
}
export interface HiPlotGraphConfig {
    axis_x: string | null;
    axis_y: string | null;
    lines_thickness: number;
    lines_opacity: number;
    dots_thickness: number;
    dots_opacity: number;
}
export declare class PlotXY extends React.Component<PlotXYProps, PlotXYState> {
    on_resize: () => void;
    params_def: ParamDefMap;
    svg: any;
    clear_canvas: () => void;
    axis_x: WatchedProperty;
    axis_y: WatchedProperty;
    config: HiPlotGraphConfig;
    root_ref: React.RefObject<HTMLDivElement>;
    canvas_lines_ref: React.RefObject<HTMLCanvasElement>;
    canvas_highlighted_ref: React.RefObject<HTMLCanvasElement>;
    constructor(props: PlotXYProps);
    static defaultProps: {
        name: string;
        data: {};
    };
    componentDidMount(): void;
    onResizeH(height: number): void;
    onWindowResize: any;
    render(): JSX.Element;
    componentWillUnmount(): void;
    componentDidUpdate(prevProps: any, prevState: any): void;
}
export {};
