import { State } from "./lib/savedstate";
import { Datapoint, ParamType, HiPlotValueDef } from "./types";
export interface ParamDef extends HiPlotValueDef {
    create_d3_scale: any;
    optional: boolean;
    numeric: boolean;
    distinct_values: Array<any>;
    colorScheme: (value: any, alpha: number) => string;
    special_values: Array<any>;
    type_options: Array<ParamType>;
    __url_state__: State;
}
export interface ParamDefMap {
    [key: string]: ParamDef;
}
/**
 * Ideally we want to infer:
 *  - If a variable is categorical
 *  - If a variable is numeric
 *  - If a variable is log-scaled
 */
export declare function infertypes(url_states: State, table: Array<Datapoint>, hints: {
    [key: string]: HiPlotValueDef;
}): ParamDefMap;
