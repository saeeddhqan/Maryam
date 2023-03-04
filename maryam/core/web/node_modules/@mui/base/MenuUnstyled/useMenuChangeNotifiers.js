import * as React from 'react';
import useMessageBus from '../utils/useMessageBus';
const HIGHLIGHT_CHANGE_TOPIC = 'menu:change-highlight';
/**
 * @ignore - internal hook.
 *
 * This hook is used to notify any interested components about changes in the Menu's selection and highlight.
 */
export default function useMenuChangeNotifiers() {
  const messageBus = useMessageBus();
  const notifyHighlightChanged = React.useCallback(newValue => {
    messageBus.publish(HIGHLIGHT_CHANGE_TOPIC, newValue);
  }, [messageBus]);
  const registerHighlightChangeHandler = React.useCallback(handler => {
    return messageBus.subscribe(HIGHLIGHT_CHANGE_TOPIC, handler);
  }, [messageBus]);
  return {
    notifyHighlightChanged,
    registerHighlightChangeHandler
  };
}