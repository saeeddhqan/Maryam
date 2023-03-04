import * as React from 'react';
export interface UseBadgeParameters {
    badgeContent?: React.ReactNode;
    invisible?: boolean;
    max?: number;
    showZero?: boolean;
}
/**
 *
 * Demos:
 *
 * - [Unstyled badge](https://mui.com/base/react-badge/#hook)
 *
 * API:
 *
 * - [useBadge API](https://mui.com/base/api/use-badge/)
 */
export default function useBadge(parameters: UseBadgeParameters): {
    badgeContent: React.ReactNode;
    invisible: boolean;
    max: number;
    displayValue: React.ReactNode;
};
