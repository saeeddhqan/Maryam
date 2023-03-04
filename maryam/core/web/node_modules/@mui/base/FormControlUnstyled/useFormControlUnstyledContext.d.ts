import * as React from 'react';
/**
 *
 * Demos:
 *
 * - [Unstyled Form Control](https://mui.com/base/react-form-control/#hook)
 *
 * API:
 *
 * - [useFormControlUnstyledContext API](https://mui.com/base/api/use-form-control-unstyled-context/)
 */
export default function useFormControlUnstyledContext(): {
    disabled?: boolean | undefined;
    required?: boolean | undefined;
    value?: unknown;
    onChange?: React.ChangeEventHandler<import("./FormControlUnstyled.types").NativeFormControlElement> | undefined;
    error?: boolean | undefined;
    filled: boolean;
    focused: boolean;
    onBlur: () => void;
    onFocus: () => void;
} | undefined;
