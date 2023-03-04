import * as React from 'react';
import useMessageBus from '../utils/useMessageBus';
var HIGHLIGHT_CHANGE_TOPIC = 'menu:change-highlight';
/**
 * @ignore - internal hook.
 *
 * This hook is used to notify any interested components about changes in the Menu's selection and highlight.
 */
export default function useMenuChangeNotifiers() {
  var messageBus = useMessageBus();
  var notifyHighlightChanged = React.useCallback(function (newValue) {
    messageBus.publish(HIGHLIGHT_CHANGE_TOPIC, newValue);
  }, [messageBus]);
  var registerHighlightChangeHandler = React.useCallback(function (handler) {
    return messageBus.subscribe(HIGHLIGHT_CHANGE_TOPIC, handler);
  }, [messageBus]);
  return {
    notifyHighlightChanged: notifyHighlightChanged,
    registerHighlightChangeHandler: registerHighlightChangeHandler
  };
}