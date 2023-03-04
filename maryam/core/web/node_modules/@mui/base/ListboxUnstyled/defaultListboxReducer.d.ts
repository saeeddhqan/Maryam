import { ListboxState, ListboxReducerAction } from './useListbox.types';
export default function defaultListboxReducer<TOption>(state: Readonly<ListboxState<TOption>>, action: ListboxReducerAction<TOption>): Readonly<ListboxState<TOption>>;
