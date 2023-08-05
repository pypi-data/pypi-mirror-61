/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
export class State {
    constructor(name) {
        this.prefix = name == '' ? '' : name + '.';
    }
    get(name, def_value) {
        return PageState.get(this.prefix + name, def_value);
    }
    set(name, value) {
        return PageState.set(this.prefix + name, value);
    }
    clear() {
        PageState.clear_all(self.name);
    }
    children(name) {
        return new State(this.prefix + name);
    }
}
;
class GlobalPageState {
    constructor() {
        this.params = {}; // In case history doesnt work, like when we are embedded in an iframe
    }
    create_state(name) {
        return new State(name);
    }
    get(name, default_value) {
        if (this.params[name] !== undefined) {
            return this.params[name];
        }
        const searchParams = new URLSearchParams(location.search);
        var value = searchParams.get(name);
        if (value === null) {
            return default_value;
        }
        return JSON.parse(value);
    }
    set(name, new_value) {
        const searchParams = new URLSearchParams(location.search);
        searchParams.set(name, JSON.stringify(new_value));
        try {
            history.replaceState({}, 'title', '?' + searchParams.toString());
        }
        catch (e) {
            this.params[name] = new_value;
        }
    }
    clear_all(prefix) {
        const searchParams = new URLSearchParams(location.search);
        for (var param_name in searchParams.keys()) {
            if (param_name.startsWith(prefix)) {
                searchParams.delete(param_name);
            }
        }
        try {
            history.replaceState({}, 'title', '?' + searchParams.toString());
        }
        catch (e) {
            this.params = {};
        }
    }
}
export var PageState = new GlobalPageState();
