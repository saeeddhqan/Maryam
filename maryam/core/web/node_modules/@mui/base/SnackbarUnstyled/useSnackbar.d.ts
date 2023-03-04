import * as React from 'react';
import { UseSnackbarParameters, UseSnackbarRootSlotProps } from './useSnackbar.types';
/**
 * The basic building block for creating custom snackbar.
 *
 * Demos:
 *
 * - [Unstyled Snackbar](https://mui.com/base/react-snackbar/#hook)
 *
 * API:
 *
 * - [useSnackbar API](https://mui.com/base/api/use-snackbar/)
 */
export default function useSnackbar(parameters: UseSnackbarParameters): {
    getRootProps: <TOther extends Record<string, ((event: any) => void) | undefined> = {}>(otherHandlers?: TOther) => UseSnackbarRootSlotProps<TOther>;
    onClickAway: (event: React.SyntheticEvent<any> | Event) => void;
};
