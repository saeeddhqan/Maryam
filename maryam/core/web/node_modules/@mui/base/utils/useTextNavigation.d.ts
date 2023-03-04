import * as React from 'react';
/**
 * @ignore - internal hook.
 *
 * Provides a handler for text navigation.
 * It's used to navigate the listbox by typing the first letters of the options.
 *
 * @param callback A function to be called when the navigation should be performed.
 * @returns A function to be used in a keydown event handler.
 */
export default function useTextNavigation(callback: (searchString: string, event: React.KeyboardEvent) => void): (event: React.KeyboardEvent) => void;
