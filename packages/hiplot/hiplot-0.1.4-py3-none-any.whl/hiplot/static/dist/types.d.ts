export interface Datapoint {
    uid: string;
    from_uid: string | null;
    [key: string]: any;
}
export interface DatapointLookup {
    [key: string]: Datapoint;
}
export declare class WatchedProperty {
    name: string;
    __on_change_handlers: Array<{
        cb: (value: any) => void;
        obj: any;
    }>;
    value: any;
    constructor(name: string);
    set(value: any): void;
    get(): any;
    on_change(cb: (value: any) => void, obj: any): void;
    off(obj: any): void;
}
export declare class Dataset {
    name: string;
    rows: Array<Datapoint>;
    on_change_fn: Array<{
        cb: (rows: Array<Datapoint>) => void;
        obj: any;
    }>;
    on_append_fn: Array<{
        cb: (rows: Array<Datapoint>) => void;
        obj: any;
    }>;
    named_childs: {
        [key: string]: Dataset;
    };
    constructor(name: string);
    set(new_rows: Array<Datapoint>): void;
    append(new_rows: Array<Datapoint>): void;
    _set(new_rows: Array<Datapoint>): void;
    _append(new_rows: Array<Datapoint>): void;
    get(): Array<Datapoint>;
    on_change(cb: (rows: Array<Datapoint>) => void, obj: any): void;
    on_append(cb: (new_rows: Array<Datapoint>) => void, obj: any): void;
    off(obj: any): void;
}
export declare class AllDatasets {
    experiment_all: Dataset;
    all: Dataset;
    selected: Dataset;
    rendered: Dataset;
    highlighted: Dataset;
    constructor(experiment_all?: Dataset, all?: Dataset, // Everything after filtering
    selected?: Dataset, // What we currently select (with parallel plot)
    rendered?: Dataset, // What we have rendered on the screen
    highlighted?: Dataset);
    off(obj: any): void;
}
export declare enum ParamType {
    CATEGORICAL = "categorical",
    NUMERIC = "numeric",
    NUMERICLOG = "numericlog",
    NUMERICPERCENTILE = "numericpercentile"
}
export interface HiPlotValueDef {
    type: ParamType;
    colors: {
        [value: string]: string;
    };
    force_value_min: number | null;
    force_value_max: number | null;
}
export interface HiPlotExperiment {
    datapoints: Array<Datapoint>;
    parameters_definition: {
        [key: string]: HiPlotValueDef;
    };
    _displays: {
        [key: string]: {
            [key2: string]: any;
        };
    };
}
export declare enum HiPlotLoadStatus {
    None = 0,
    Loading = 1,
    Loaded = 2,
    Error = 3
}
export declare const URL_LOAD_URI = "load_uri";
export declare const URL_COLOR_BY = "color_by";
