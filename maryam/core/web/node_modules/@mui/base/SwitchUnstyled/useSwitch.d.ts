import * as React from 'react';
import { UseSwitchInputSlotProps, UseSwitchParameters } from './useSwitch.types';
/**
 * The basic building block for creating custom switches.
 *
 * Demos:
 *
 * - [Unstyled Switch](https://mui.com/base/react-switch/#hook)
 *
 * API:
 *
 * - [useSwitch API](https://mui.com/base/api/use-switch/)
 */
export default function useSwitch(props: UseSwitchParameters): {
    checked: boolean;
    disabled: boolean;
    focusVisible: boolean;
    getInputProps: (otherProps?: React.HTMLAttributes<HTMLInputElement>) => UseSwitchInputSlotProps;
    readOnly: boolean;
};
