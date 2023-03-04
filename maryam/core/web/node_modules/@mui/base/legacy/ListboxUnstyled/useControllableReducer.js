import _extends from "@babel/runtime/helpers/esm/extends";
import * as React from 'react';
import { ActionTypes } from './useListbox.types';
import areArraysEqual from '../utils/areArraysEqual';

/**
 * Gets the current state. If the selectedValue is controlled,
 * the `value` prop is the source of truth instead of the internal state.
 */
function getControlledState(internalState, props) {
  if (props.value !== undefined) {
    return _extends({}, internalState, {
      selectedValue: props.value
    });
  }
  return internalState;
}
function areOptionsEqual(option1, option2, optionComparer) {
  if (option1 === option2) {
    return true;
  }
  if (option1 === null || option2 === null) {
    return false;
  }
  return optionComparer(option1, option2);
}

/**
 * Triggers change event handlers (onChange and onHighlightChange) when reducer returns changed state.
 *
 * @param nextState The next state returned by the reducer.
 * @param internalPreviousState The previous state. If the component is controlled, this is merged with the props to determine the final state.
 * @param propsRef The props with defaults applied.
 * @param lastActionRef The last action that was dispatched.
 */
function useStateChangeDetection(nextState, internalPreviousState, propsRef, lastActionRef) {
  React.useEffect(function () {
    if (!propsRef.current || lastActionRef.current === null) {
      // Detect changes only if an action has been dispatched.
      return;
    }
    if (lastActionRef.current.type === ActionTypes.setValue || lastActionRef.current.type === ActionTypes.setHighlight) {
      // Don't fire change events when the value has been changed externally (e.g. by changing the controlled prop).
      return;
    }
    var previousState = getControlledState(internalPreviousState, propsRef.current);
    var _propsRef$current = propsRef.current,
      multiple = _propsRef$current.multiple,
      optionComparer = _propsRef$current.optionComparer;
    if (multiple) {
      var _previousState$select;
      var previousSelectedValues = (_previousState$select = previousState == null ? void 0 : previousState.selectedValue) != null ? _previousState$select : [];
      var nextSelectedValues = nextState.selectedValue;
      var onChange = propsRef.current.onChange;
      if (!areArraysEqual(nextSelectedValues, previousSelectedValues, optionComparer)) {
        onChange == null ? void 0 : onChange(lastActionRef.current.event, nextSelectedValues);
      }
    } else {
      var previousSelectedValue = previousState == null ? void 0 : previousState.selectedValue;
      var nextSelectedValue = nextState.selectedValue;
      var _onChange = propsRef.current.onChange;
      if (!areOptionsEqual(nextSelectedValue, previousSelectedValue, optionComparer)) {
        _onChange == null ? void 0 : _onChange(lastActionRef.current.event, nextSelectedValue);
      }
    }

    // Fires the highlightChange event when reducer returns changed `highlightedValue`.
    if (!areOptionsEqual(internalPreviousState.highlightedValue, nextState.highlightedValue, propsRef.current.optionComparer)) {
      var _propsRef$current2, _propsRef$current2$on;
      (_propsRef$current2 = propsRef.current) == null ? void 0 : (_propsRef$current2$on = _propsRef$current2.onHighlightChange) == null ? void 0 : _propsRef$current2$on.call(_propsRef$current2, lastActionRef.current.event, nextState.highlightedValue);
    }
    lastActionRef.current = null;
  }, [nextState.selectedValue, nextState.highlightedValue, internalPreviousState, propsRef, lastActionRef]);
}

/**
 * @ignore - do not document.
 */
export default function useControllableReducer(internalReducer, externalReducer, props) {
  var _ref2;
  var _ref = props.current,
    value = _ref.value,
    defaultValue = _ref.defaultValue,
    multiple = _ref.multiple;
  var actionRef = React.useRef(null);
  var initialSelectedValue = (_ref2 = value === undefined ? defaultValue : value) != null ? _ref2 : multiple ? [] : null;
  var initialState = {
    highlightedValue: null,
    selectedValue: initialSelectedValue
  };
  var combinedReducer = React.useCallback(function (state, action) {
    actionRef.current = action;
    if (externalReducer) {
      return externalReducer(getControlledState(state, action.props), action);
    }
    return internalReducer(getControlledState(state, action.props), action);
  }, [externalReducer, internalReducer]);
  var _React$useReducer = React.useReducer(combinedReducer, initialState),
    nextState = _React$useReducer[0],
    dispatch = _React$useReducer[1];
  var dispatchWithProps = React.useCallback(function (action) {
    dispatch(_extends({
      props: props.current
    }, action));
  }, [dispatch, props]);
  var previousState = React.useRef(initialState);
  React.useEffect(function () {
    previousState.current = nextState;
  }, [previousState, nextState]);
  useStateChangeDetection(nextState, previousState.current, props, actionRef);
  return [getControlledState(nextState, props.current), dispatchWithProps];
}