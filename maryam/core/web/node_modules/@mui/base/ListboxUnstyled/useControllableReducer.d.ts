import * as React from 'react';
import { ListboxAction, ListboxReducer, ListboxState, UseListboxPropsWithDefaults } from './useListbox.types';
/**
 * @ignore - do not document.
 */
export default function useControllableReducer<TOption>(internalReducer: ListboxReducer<TOption>, externalReducer: ListboxReducer<TOption> | undefined, props: React.RefObject<UseListboxPropsWithDefaults<TOption>>): [ListboxState<TOption>, (action: ListboxAction<TOption>) => void];
