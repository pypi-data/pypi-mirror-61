import React from "react";
import { HiPlotLoadStatus } from "./types";
import { HiPlotPluginData } from "./plugin";
interface Props {
    onSubmit: (content: string) => void;
    enabled: boolean;
    initialValue: string;
    minimizeWhenOutOfFocus: boolean;
    onFocusChange: (hasFocus: boolean) => void;
    hasFocus: boolean;
}
interface State {
    value: string;
}
export declare class RunsSelectionTextArea extends React.Component<Props, State> {
    container: React.RefObject<HTMLDivElement>;
    textarea: React.RefObject<HTMLTextAreaElement>;
    constructor(props: Props);
    onInput(): void;
    onKeyDown(evt: React.KeyboardEvent<HTMLTextAreaElement>): void;
    onFocusChange(evt: React.FocusEvent<HTMLTextAreaElement>): void;
    componentDidMount(): void;
    componentDidUpdate(): void;
    render(): JSX.Element;
}
interface HeaderBarProps extends HiPlotPluginData {
    onRequestLoadExperiment?: (uri: string) => void;
    onRequestRefreshExperiment?: () => void;
    loadStatus: HiPlotLoadStatus;
}
interface HeaderBarState {
    isTextareaFocused: boolean;
    hasTutorial: boolean;
}
export declare class HeaderBar extends React.Component<HeaderBarProps, HeaderBarState> {
    selected_count_ref: React.RefObject<HTMLElement>;
    selected_pct_ref: React.RefObject<HTMLElement>;
    total_count_ref: React.RefObject<HTMLElement>;
    controls_root_ref: React.RefObject<HTMLDivElement>;
    constructor(props: HeaderBarProps);
    recomputeMetrics(): void;
    componentDidMount(): void;
    componentWillUnmount(): void;
    componentDidUpdate(): void;
    onToggleTutorial(): void;
    renderControls(): JSX.Element;
    render(): JSX.Element;
}
interface ErrorDisplayProps {
    error: string;
}
export declare class ErrorDisplay extends React.Component<ErrorDisplayProps> {
    render(): JSX.Element;
}
export {};
