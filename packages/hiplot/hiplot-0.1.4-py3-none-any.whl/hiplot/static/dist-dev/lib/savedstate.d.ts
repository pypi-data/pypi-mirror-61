export declare class State {
    prefix: string;
    constructor(name: string);
    get(name: string, def_value?: any): any;
    set(name: string, value: any): void;
    clear(): void;
    children(name: string): State;
}
declare class GlobalPageState {
    params: {};
    create_state(name: string): State;
    get(name: string, default_value?: any): any;
    set(name: string, new_value: any): void;
    clear_all(prefix: string): void;
}
export declare var PageState: GlobalPageState;
export {};
