import * as React from 'react';
import useMessageBus from '../utils/useMessageBus';
const SELECTION_CHANGE_TOPIC = 'select:change-selection';
const HIGHLIGHT_CHANGE_TOPIC = 'select:change-highlight';
/**
 * @ignore - internal hook.
 *
 * This hook is used to notify any interested components about changes in the Select's selection and highlight.
 */
export default function useSelectChangeNotifiers() {
  const messageBus = useMessageBus();
  const notifySelectionChanged = React.useCallback(newValue => {
    messageBus.publish(SELECTION_CHANGE_TOPIC, newValue);
  }, [messageBus]);
  const notifyHighlightChanged = React.useCallback(newValue => {
    messageBus.publish(HIGHLIGHT_CHANGE_TOPIC, newValue);
  }, [messageBus]);
  const registerSelectionChangeHandler = React.useCallback(handler => {
    return messageBus.subscribe(SELECTION_CHANGE_TOPIC, handler);
  }, [messageBus]);
  const registerHighlightChangeHandler = React.useCallback(handler => {
    return messageBus.subscribe(HIGHLIGHT_CHANGE_TOPIC, handler);
  }, [messageBus]);
  return {
    notifySelectionChanged,
    notifyHighlightChanged,
    registerSelectionChangeHandler,
    registerHighlightChangeHandler
  };
}