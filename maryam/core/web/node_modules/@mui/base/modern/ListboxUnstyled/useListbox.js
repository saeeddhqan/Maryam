import _extends from "@babel/runtime/helpers/esm/extends";
import * as React from 'react';
import { unstable_useForkRef as useForkRef, unstable_useId as useId } from '@mui/utils';
import { ActionTypes } from './useListbox.types';
import defaultReducer from './defaultListboxReducer';
import useControllableReducer from './useControllableReducer';
import areArraysEqual from '../utils/areArraysEqual';
import useLatest from '../utils/useLatest';
import useTextNavigation from '../utils/useTextNavigation';
const defaultOptionComparer = (optionA, optionB) => optionA === optionB;
const defaultIsOptionDisabled = () => false;
const defaultOptionStringifier = option => typeof option === 'string' ? option : String(option);

/**
 * @ignore - do not document.
 */
export default function useListbox(props) {
  const {
    disabledItemsFocusable = false,
    disableListWrap = false,
    focusManagement = 'activeDescendant',
    id: idProp,
    isOptionDisabled = defaultIsOptionDisabled,
    listboxRef: externalListboxRef,
    multiple = false,
    optionComparer = defaultOptionComparer,
    optionStringifier = defaultOptionStringifier,
    options,
    stateReducer: externalReducer,
    value: valueParam
  } = props;
  const id = useId(idProp);
  const defaultIdGenerator = React.useCallback((_, index) => `${id}-option-${index}`, [id]);
  const optionIdGenerator = props.optionIdGenerator ?? defaultIdGenerator;
  const propsWithDefaults = useLatest(_extends({}, props, {
    disabledItemsFocusable,
    disableListWrap,
    focusManagement,
    isOptionDisabled,
    multiple,
    optionComparer,
    optionStringifier
  }), [props]);
  const listboxRef = React.useRef(null);
  const handleRef = useForkRef(externalListboxRef, listboxRef);
  const [{
    highlightedValue,
    selectedValue
  }, dispatch] = useControllableReducer(defaultReducer, externalReducer, propsWithDefaults);
  const handleTextNavigation = useTextNavigation((searchString, event) => dispatch({
    type: ActionTypes.textNavigation,
    event,
    searchString
  }));
  React.useEffect(() => {
    // if a controlled value changes, we need to update the state to keep things in sync
    if (valueParam !== undefined && valueParam !== selectedValue) {
      dispatch({
        type: ActionTypes.setValue,
        event: null,
        value: valueParam
      });
    }
  }, [valueParam, selectedValue, dispatch]);
  const highlightedIndex = React.useMemo(() => {
    return highlightedValue == null ? -1 : options.findIndex(option => optionComparer(option, highlightedValue));
  }, [highlightedValue, options, optionComparer]);

  // introducing refs to avoid recreating the getOptionState function on each change.
  const latestSelectedValue = useLatest(selectedValue);
  const latestHighlightedIndex = useLatest(highlightedIndex);
  const previousOptions = React.useRef([]);
  React.useEffect(() => {
    if (areArraysEqual(previousOptions.current, options, optionComparer)) {
      return;
    }
    dispatch({
      type: ActionTypes.optionsChange,
      event: null,
      options,
      previousOptions: previousOptions.current
    });
    previousOptions.current = options;
  }, [options, optionComparer, dispatch]);
  const setSelectedValue = React.useCallback(option => {
    dispatch({
      type: ActionTypes.setValue,
      event: null,
      value: option
    });
  }, [dispatch]);
  const setHighlightedValue = React.useCallback(option => {
    dispatch({
      type: ActionTypes.setHighlight,
      event: null,
      highlight: option
    });
  }, [dispatch]);
  const createHandleOptionClick = React.useCallback((option, other) => event => {
    other.onClick?.(event);
    if (event.defaultPrevented) {
      return;
    }
    event.preventDefault();
    dispatch({
      type: ActionTypes.optionClick,
      option,
      event
    });
  }, [dispatch]);
  const createHandleOptionPointerOver = React.useCallback((option, other) => event => {
    other.onMouseOver?.(event);
    if (event.defaultPrevented) {
      return;
    }
    dispatch({
      type: ActionTypes.optionHover,
      option,
      event
    });
  }, [dispatch]);
  const createHandleKeyDown = other => event => {
    other.onKeyDown?.(event);
    if (event.defaultPrevented) {
      return;
    }
    const keysToPreventDefault = ['ArrowUp', 'ArrowDown', 'Home', 'End', 'PageUp', 'PageDown'];
    if (focusManagement === 'activeDescendant') {
      // When the child element is focused using the activeDescendant attribute,
      // the listbox handles keyboard events on its behalf.
      // We have to `preventDefault()` is this case to prevent the browser from
      // scrolling the view when space is pressed or submitting forms when enter is pressed.
      keysToPreventDefault.push(' ', 'Enter');
    }
    if (keysToPreventDefault.includes(event.key)) {
      event.preventDefault();
    }
    dispatch({
      type: ActionTypes.keyDown,
      event
    });
    handleTextNavigation(event);
  };
  const createHandleBlur = other => event => {
    other.onBlur?.(event);
    if (event.defaultPrevented) {
      return;
    }
    if (listboxRef.current?.contains(document.activeElement)) {
      // focus is within the listbox
      return;
    }
    dispatch({
      type: ActionTypes.blur,
      event
    });
  };
  const getRootProps = (otherHandlers = {}) => {
    return _extends({}, otherHandlers, {
      'aria-activedescendant': focusManagement === 'activeDescendant' && highlightedValue != null ? optionIdGenerator(highlightedValue, highlightedIndex) : undefined,
      id,
      onBlur: createHandleBlur(otherHandlers),
      onKeyDown: createHandleKeyDown(otherHandlers),
      role: 'listbox',
      tabIndex: focusManagement === 'DOM' ? -1 : 0,
      ref: handleRef
    });
  };
  const getOptionState = React.useCallback(option => {
    let selected;
    const index = options.findIndex(opt => optionComparer(opt, option));
    if (multiple) {
      selected = (latestSelectedValue.current ?? []).some(value => value != null && optionComparer(option, value));
    } else {
      selected = optionComparer(option, latestSelectedValue.current);
    }
    const disabled = isOptionDisabled(option, index);
    const highlighted = latestHighlightedIndex.current === index && index !== -1;
    return {
      disabled,
      highlighted,
      index,
      selected
    };
  }, [options, multiple, isOptionDisabled, optionComparer, latestSelectedValue, latestHighlightedIndex]);
  const getOptionTabIndex = React.useCallback(optionState => {
    if (focusManagement === 'activeDescendant') {
      return undefined;
    }
    if (!optionState.highlighted) {
      return -1;
    }
    if (optionState.disabled && !disabledItemsFocusable) {
      return -1;
    }
    return 0;
  }, [focusManagement, disabledItemsFocusable]);
  const getOptionProps = React.useCallback((option, otherHandlers = {}) => {
    const optionState = getOptionState(option);
    return _extends({}, otherHandlers, {
      'aria-disabled': optionState.disabled || undefined,
      'aria-selected': optionState.selected,
      id: optionIdGenerator(option, optionState.index),
      onClick: createHandleOptionClick(option, otherHandlers),
      onPointerOver: createHandleOptionPointerOver(option, otherHandlers),
      role: 'option',
      tabIndex: getOptionTabIndex(optionState)
    });
  }, [optionIdGenerator, createHandleOptionClick, createHandleOptionPointerOver, getOptionTabIndex, getOptionState]);
  React.useDebugValue({
    highlightedOption: highlightedValue,
    selectedOption: selectedValue
  });
  return {
    getRootProps,
    getOptionProps,
    getOptionState,
    highlightedOption: highlightedValue,
    selectedOption: selectedValue,
    setSelectedValue,
    setHighlightedValue
  };
}