import React from "react";
interface ResizableHProps {
    initialHeight: number;
    onResize: (height: number) => void;
    borderSize: number;
    minHeight: number;
}
interface ResizableHState {
    height: number;
    internalHeight: number;
}
export declare class ResizableH extends React.Component<ResizableHProps, ResizableHState> {
    div_ref: React.RefObject<HTMLDivElement>;
    m_pos: number;
    constructor(props: ResizableHProps);
    static defaultProps: {
        borderSize: number;
        minHeight: number;
    };
    componentDidMount(): void;
    componentDidUpdate(prevProps: any, prevState: any): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
    onMouseMove: any;
    onMouseUp: any;
}
export {};
