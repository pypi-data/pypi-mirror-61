import React from "react";
import { AllDatasets } from "./types";
interface HiPlotDataControlProps {
    rows: AllDatasets;
}
interface HiPlotDataControlState {
    btnEnabled: boolean;
}
export declare class KeepDataBtn extends React.Component<HiPlotDataControlProps, HiPlotDataControlState> {
    btnRef: React.RefObject<HTMLButtonElement>;
    constructor(props: HiPlotDataControlProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
export declare class ExcludeDataBtn extends React.Component<HiPlotDataControlProps, HiPlotDataControlState> {
    constructor(props: HiPlotDataControlProps);
    componentDidMount(): void;
    onClick(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
export declare class ExportDataCSVBtn extends React.Component<HiPlotDataControlProps, HiPlotDataControlState> {
    onClick(): void;
    render(): JSX.Element;
}
export declare class RestoreDataBtn extends React.Component<HiPlotDataControlProps, HiPlotDataControlState> {
    constructor(props: HiPlotDataControlProps);
    componentDidMount(): void;
    componentWillUnmount(): void;
    onClick(): void;
    render(): JSX.Element;
}
export declare class SelectedCountProgressBar extends React.Component<HiPlotDataControlProps, HiPlotDataControlState> {
    selectedBar: React.RefObject<HTMLDivElement>;
    renderedBar: React.RefObject<HTMLDivElement>;
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
interface ThemeToggleProps {
    root: React.RefObject<HTMLElement>;
}
interface ThemeToggleState {
    dark: boolean;
}
export declare class ThemeToggle extends React.Component<ThemeToggleProps, ThemeToggleState> {
    btnRef: React.RefObject<HTMLButtonElement>;
    constructor(props: any);
    onClick(): void;
    componentDidUpdate(): void;
    render(): JSX.Element;
}
export {};
