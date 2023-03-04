import * as React from 'react';
import useMessageBus from '../utils/useMessageBus';
var SELECTION_CHANGE_TOPIC = 'select:change-selection';
var HIGHLIGHT_CHANGE_TOPIC = 'select:change-highlight';
/**
 * @ignore - internal hook.
 *
 * This hook is used to notify any interested components about changes in the Select's selection and highlight.
 */
export default function useSelectChangeNotifiers() {
  var messageBus = useMessageBus();
  var notifySelectionChanged = React.useCallback(function (newValue) {
    messageBus.publish(SELECTION_CHANGE_TOPIC, newValue);
  }, [messageBus]);
  var notifyHighlightChanged = React.useCallback(function (newValue) {
    messageBus.publish(HIGHLIGHT_CHANGE_TOPIC, newValue);
  }, [messageBus]);
  var registerSelectionChangeHandler = React.useCallback(function (handler) {
    return messageBus.subscribe(SELECTION_CHANGE_TOPIC, handler);
  }, [messageBus]);
  var registerHighlightChangeHandler = React.useCallback(function (handler) {
    return messageBus.subscribe(HIGHLIGHT_CHANGE_TOPIC, handler);
  }, [messageBus]);
  return {
    notifySelectionChanged: notifySelectionChanged,
    notifyHighlightChanged: notifyHighlightChanged,
    registerSelectionChangeHandler: registerSelectionChangeHandler,
    registerHighlightChangeHandler: registerHighlightChangeHandler
  };
}