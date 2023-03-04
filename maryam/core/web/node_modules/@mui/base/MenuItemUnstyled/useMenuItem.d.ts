import * as React from 'react';
import { EventHandlers } from '../utils/types';
import { UseMenuItemParameters } from './useMenuItem.types';
/**
 *
 * Demos:
 *
 * - [Unstyled Menu](https://mui.com/base/react-menu/#hooks)
 *
 * API:
 *
 * - [useMenuItem API](https://mui.com/base/api/use-menu-item/)
 */
export default function useMenuItem(props: UseMenuItemParameters): {
    getRootProps: (other?: EventHandlers) => {
        role: string;
        'aria-disabled'?: (boolean | "false" | "true") | undefined;
        disabled?: boolean | undefined;
        tabIndex?: number | undefined;
        type?: "button" | "reset" | "submit" | undefined;
        onBlur: React.FocusEventHandler<Element>;
        onFocus: React.FocusEventHandler<Element>;
        onKeyDown: React.KeyboardEventHandler<Element>;
        onKeyUp: React.KeyboardEventHandler<Element>;
        onMouseDown: React.MouseEventHandler<Element>;
        onMouseLeave: React.MouseEventHandler<Element>;
        ref: React.Ref<any>;
    };
    disabled: boolean;
    focusVisible: boolean;
    highlighted: boolean;
} | {
    getRootProps: (other?: EventHandlers) => {
        tabIndex: any;
        id: any;
        role: string;
        'aria-disabled'?: (boolean | "false" | "true") | undefined;
        disabled?: boolean | undefined;
        type?: "button" | "reset" | "submit" | undefined;
        onBlur: React.FocusEventHandler<Element>;
        onFocus: React.FocusEventHandler<Element>;
        onKeyDown: React.KeyboardEventHandler<Element>;
        onKeyUp: React.KeyboardEventHandler<Element>;
        onMouseDown: React.MouseEventHandler<Element>;
        onMouseLeave: React.MouseEventHandler<Element>;
        ref: React.Ref<any>;
    };
    disabled: boolean;
    focusVisible: boolean;
    highlighted: boolean;
};
