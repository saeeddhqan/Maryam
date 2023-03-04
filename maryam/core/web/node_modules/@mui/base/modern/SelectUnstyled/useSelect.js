import _extends from "@babel/runtime/helpers/esm/extends";
import * as React from 'react';
import { unstable_useForkRef as useForkRef, unstable_useId as useId } from '@mui/utils';
import { useButton } from '../ButtonUnstyled';
import { useListbox, defaultListboxReducer, ActionTypes } from '../ListboxUnstyled';
import defaultOptionStringifier from './defaultOptionStringifier';
import useSelectChangeNotifiers from './useSelectChangeNotifiers';
/**
 *
 * Demos:
 *
 * - [Unstyled Select](https://mui.com/base/react-select/#hook)
 *
 * API:
 *
 * - [useSelect API](https://mui.com/base/api/use-select/)
 */
function useSelect(props) {
  const {
    buttonRef: buttonRefProp,
    defaultValue: defaultValueProp,
    disabled = false,
    listboxId: listboxIdProp,
    listboxRef: listboxRefProp,
    multiple = false,
    onChange,
    onHighlightChange,
    onOpenChange,
    open = false,
    options,
    optionStringifier = defaultOptionStringifier,
    value: valueProp
  } = props;
  const buttonRef = React.useRef(null);
  const handleButtonRef = useForkRef(buttonRefProp, buttonRef);
  const listboxRef = React.useRef(null);
  const listboxId = useId(listboxIdProp);
  let defaultValue = defaultValueProp;
  if (valueProp === undefined && defaultValueProp === undefined) {
    defaultValue = multiple ? [] : null;
  }
  const optionsMap = React.useMemo(() => {
    const map = new Map();
    options.forEach(option => {
      map.set(option.value, option);
    });
    return map;
  }, [options]);

  // prevents closing the listbox on keyUp right after opening it
  const ignoreEnterKeyUp = React.useRef(false);

  // prevents reopening the listbox when button is clicked
  // (listbox closes on lost focus, then immediately reopens on click)
  const ignoreClick = React.useRef(false);

  // Ensure the listbox is focused after opening
  const [listboxFocusRequested, requestListboxFocus] = React.useState(false);
  const focusListboxIfRequested = React.useCallback(() => {
    if (listboxFocusRequested && listboxRef.current != null) {
      listboxRef.current.focus();
      requestListboxFocus(false);
    }
  }, [listboxFocusRequested]);
  const handleListboxRef = useForkRef(listboxRefProp, listboxRef, focusListboxIfRequested);
  const {
    notifySelectionChanged,
    notifyHighlightChanged,
    registerHighlightChangeHandler,
    registerSelectionChangeHandler
  } = useSelectChangeNotifiers();
  React.useEffect(() => {
    focusListboxIfRequested();
  }, [focusListboxIfRequested]);
  React.useEffect(() => {
    requestListboxFocus(open);
  }, [open]);
  const createHandleMouseDown = otherHandlers => event => {
    otherHandlers?.onMouseDown?.(event);
    if (!event.defaultPrevented && open) {
      ignoreClick.current = true;
    }
  };
  const createHandleButtonClick = otherHandlers => event => {
    otherHandlers?.onClick?.(event);
    if (!event.defaultPrevented && !ignoreClick.current) {
      onOpenChange?.(!open);
    }
    ignoreClick.current = false;
  };
  const createHandleButtonKeyDown = otherHandlers => event => {
    otherHandlers?.onKeyDown?.(event);
    if (event.defaultPrevented) {
      return;
    }
    if (event.key === 'Enter') {
      ignoreEnterKeyUp.current = true;
    }
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      onOpenChange?.(true);
    }
  };
  const createHandleListboxKeyUp = otherHandlers => event => {
    otherHandlers?.onKeyUp?.(event);
    if (event.defaultPrevented) {
      return;
    }
    const closingKeys = multiple ? ['Escape'] : ['Escape', 'Enter', ' '];
    if (open && !ignoreEnterKeyUp.current && closingKeys.includes(event.key)) {
      buttonRef?.current?.focus();
    }
    ignoreEnterKeyUp.current = false;
  };
  const createHandleListboxItemClick = React.useCallback(otherHandlers => event => {
    otherHandlers?.onClick?.(event);
    if (event.defaultPrevented) {
      return;
    }
    if (!multiple) {
      onOpenChange?.(false);
    }
  }, [multiple, onOpenChange]);
  const createHandleListboxBlur = otherHandlers => event => {
    otherHandlers?.onBlur?.(event);
    if (!event.defaultPrevented) {
      onOpenChange?.(false);
    }
  };
  const listboxReducer = React.useCallback((state, action) => {
    const newState = defaultListboxReducer(state, action);

    // change selection when listbox is closed
    if (action.type === ActionTypes.keyDown && !open && (action.event.key === 'ArrowUp' || action.event.key === 'ArrowDown')) {
      return _extends({}, newState, {
        selectedValue: newState.highlightedValue
      });
    }
    if (action.type === ActionTypes.blur || action.type === ActionTypes.setValue || action.type === ActionTypes.optionsChange) {
      return _extends({}, newState, {
        highlightedValue: newState.selectedValue
      });
    }
    return newState;
  }, [open]);
  const {
    getRootProps: getButtonRootProps,
    active: buttonActive,
    focusVisible: buttonFocusVisible
  } = useButton({
    disabled,
    ref: handleButtonRef
  });
  const optionValues = React.useMemo(() => options.map(o => o.value), [options]);
  let useListboxParameters;
  const isOptionDisabled = React.useCallback(valueToCheck => {
    const option = optionsMap.get(valueToCheck);
    return option?.disabled ?? false;
  }, [optionsMap]);
  const stringifyOption = React.useCallback(valueToCheck => {
    const option = optionsMap.get(valueToCheck);
    if (!option) {
      return '';
    }
    return optionStringifier(option);
  }, [optionsMap, optionStringifier]);
  if (props.multiple) {
    const onChangeMultiple = onChange;
    useListboxParameters = {
      defaultValue: defaultValue,
      id: listboxId,
      isOptionDisabled,
      listboxRef: handleListboxRef,
      multiple: true,
      onChange: (e, newValues) => {
        onChangeMultiple?.(e, newValues);
      },
      onHighlightChange: (e, newValue) => {
        onHighlightChange?.(e, newValue ?? null);
      },
      options: optionValues,
      optionStringifier: stringifyOption,
      value: valueProp
    };
  } else {
    const onChangeSingle = onChange;
    useListboxParameters = {
      defaultValue: defaultValue,
      id: listboxId,
      isOptionDisabled,
      listboxRef: handleListboxRef,
      multiple: false,
      onChange: (e, newValue) => {
        onChangeSingle?.(e, newValue);
      },
      onHighlightChange: (e, newValue) => {
        onHighlightChange?.(e, newValue);
      },
      options: optionValues,
      optionStringifier: stringifyOption,
      stateReducer: listboxReducer,
      value: valueProp
    };
  }
  const {
    getRootProps: getListboxRootProps,
    getOptionProps: getListboxOptionProps,
    getOptionState,
    highlightedOption,
    selectedOption
  } = useListbox(useListboxParameters);
  React.useEffect(() => {
    notifySelectionChanged(selectedOption);
  }, [selectedOption, notifySelectionChanged]);
  React.useEffect(() => {
    notifyHighlightChanged(highlightedOption);
  }, [highlightedOption, notifyHighlightChanged]);
  const getButtonProps = (otherHandlers = {}) => {
    return _extends({}, getButtonRootProps(_extends({}, otherHandlers, {
      onClick: createHandleButtonClick(otherHandlers),
      onMouseDown: createHandleMouseDown(otherHandlers),
      onKeyDown: createHandleButtonKeyDown(otherHandlers)
    })), {
      role: 'combobox',
      'aria-expanded': open,
      'aria-haspopup': 'listbox',
      'aria-controls': listboxId
    });
  };
  const getListboxProps = (otherHandlers = {}) => getListboxRootProps(_extends({}, otherHandlers, {
    onBlur: createHandleListboxBlur(otherHandlers),
    onKeyUp: createHandleListboxKeyUp(otherHandlers)
  }));
  const getOptionProps = React.useCallback((optionValue, otherHandlers = {}) => {
    return getListboxOptionProps(optionValue, _extends({}, otherHandlers, {
      onClick: createHandleListboxItemClick(otherHandlers)
    }));
  }, [getListboxOptionProps, createHandleListboxItemClick]);
  React.useDebugValue({
    selectedOption,
    highlightedOption,
    open
  });
  const contextValue = React.useMemo(() => ({
    listboxRef,
    getOptionProps,
    getOptionState,
    registerHighlightChangeHandler,
    registerSelectionChangeHandler
  }), [getOptionProps, getOptionState, registerHighlightChangeHandler, registerSelectionChangeHandler]);
  return {
    buttonActive,
    buttonFocusVisible,
    disabled,
    getButtonProps,
    getListboxProps,
    contextValue,
    open,
    value: selectedOption,
    highlightedOption
  };
}
export default useSelect;