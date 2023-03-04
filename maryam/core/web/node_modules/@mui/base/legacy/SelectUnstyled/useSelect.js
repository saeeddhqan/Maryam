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
  var buttonRefProp = props.buttonRef,
    defaultValueProp = props.defaultValue,
    _props$disabled = props.disabled,
    disabled = _props$disabled === void 0 ? false : _props$disabled,
    listboxIdProp = props.listboxId,
    listboxRefProp = props.listboxRef,
    _props$multiple = props.multiple,
    multiple = _props$multiple === void 0 ? false : _props$multiple,
    onChange = props.onChange,
    _onHighlightChange = props.onHighlightChange,
    onOpenChange = props.onOpenChange,
    _props$open = props.open,
    open = _props$open === void 0 ? false : _props$open,
    options = props.options,
    _props$optionStringif = props.optionStringifier,
    optionStringifier = _props$optionStringif === void 0 ? defaultOptionStringifier : _props$optionStringif,
    valueProp = props.value;
  var buttonRef = React.useRef(null);
  var handleButtonRef = useForkRef(buttonRefProp, buttonRef);
  var listboxRef = React.useRef(null);
  var listboxId = useId(listboxIdProp);
  var defaultValue = defaultValueProp;
  if (valueProp === undefined && defaultValueProp === undefined) {
    defaultValue = multiple ? [] : null;
  }
  var optionsMap = React.useMemo(function () {
    var map = new Map();
    options.forEach(function (option) {
      map.set(option.value, option);
    });
    return map;
  }, [options]);

  // prevents closing the listbox on keyUp right after opening it
  var ignoreEnterKeyUp = React.useRef(false);

  // prevents reopening the listbox when button is clicked
  // (listbox closes on lost focus, then immediately reopens on click)
  var ignoreClick = React.useRef(false);

  // Ensure the listbox is focused after opening
  var _React$useState = React.useState(false),
    listboxFocusRequested = _React$useState[0],
    requestListboxFocus = _React$useState[1];
  var focusListboxIfRequested = React.useCallback(function () {
    if (listboxFocusRequested && listboxRef.current != null) {
      listboxRef.current.focus();
      requestListboxFocus(false);
    }
  }, [listboxFocusRequested]);
  var handleListboxRef = useForkRef(listboxRefProp, listboxRef, focusListboxIfRequested);
  var _useSelectChangeNotif = useSelectChangeNotifiers(),
    notifySelectionChanged = _useSelectChangeNotif.notifySelectionChanged,
    notifyHighlightChanged = _useSelectChangeNotif.notifyHighlightChanged,
    registerHighlightChangeHandler = _useSelectChangeNotif.registerHighlightChangeHandler,
    registerSelectionChangeHandler = _useSelectChangeNotif.registerSelectionChangeHandler;
  React.useEffect(function () {
    focusListboxIfRequested();
  }, [focusListboxIfRequested]);
  React.useEffect(function () {
    requestListboxFocus(open);
  }, [open]);
  var createHandleMouseDown = function createHandleMouseDown(otherHandlers) {
    return function (event) {
      var _otherHandlers$onMous;
      otherHandlers == null ? void 0 : (_otherHandlers$onMous = otherHandlers.onMouseDown) == null ? void 0 : _otherHandlers$onMous.call(otherHandlers, event);
      if (!event.defaultPrevented && open) {
        ignoreClick.current = true;
      }
    };
  };
  var createHandleButtonClick = function createHandleButtonClick(otherHandlers) {
    return function (event) {
      var _otherHandlers$onClic;
      otherHandlers == null ? void 0 : (_otherHandlers$onClic = otherHandlers.onClick) == null ? void 0 : _otherHandlers$onClic.call(otherHandlers, event);
      if (!event.defaultPrevented && !ignoreClick.current) {
        onOpenChange == null ? void 0 : onOpenChange(!open);
      }
      ignoreClick.current = false;
    };
  };
  var createHandleButtonKeyDown = function createHandleButtonKeyDown(otherHandlers) {
    return function (event) {
      var _otherHandlers$onKeyD;
      otherHandlers == null ? void 0 : (_otherHandlers$onKeyD = otherHandlers.onKeyDown) == null ? void 0 : _otherHandlers$onKeyD.call(otherHandlers, event);
      if (event.defaultPrevented) {
        return;
      }
      if (event.key === 'Enter') {
        ignoreEnterKeyUp.current = true;
      }
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        onOpenChange == null ? void 0 : onOpenChange(true);
      }
    };
  };
  var createHandleListboxKeyUp = function createHandleListboxKeyUp(otherHandlers) {
    return function (event) {
      var _otherHandlers$onKeyU;
      otherHandlers == null ? void 0 : (_otherHandlers$onKeyU = otherHandlers.onKeyUp) == null ? void 0 : _otherHandlers$onKeyU.call(otherHandlers, event);
      if (event.defaultPrevented) {
        return;
      }
      var closingKeys = multiple ? ['Escape'] : ['Escape', 'Enter', ' '];
      if (open && !ignoreEnterKeyUp.current && closingKeys.includes(event.key)) {
        var _buttonRef$current;
        buttonRef == null ? void 0 : (_buttonRef$current = buttonRef.current) == null ? void 0 : _buttonRef$current.focus();
      }
      ignoreEnterKeyUp.current = false;
    };
  };
  var createHandleListboxItemClick = React.useCallback(function (otherHandlers) {
    return function (event) {
      var _otherHandlers$onClic2;
      otherHandlers == null ? void 0 : (_otherHandlers$onClic2 = otherHandlers.onClick) == null ? void 0 : _otherHandlers$onClic2.call(otherHandlers, event);
      if (event.defaultPrevented) {
        return;
      }
      if (!multiple) {
        onOpenChange == null ? void 0 : onOpenChange(false);
      }
    };
  }, [multiple, onOpenChange]);
  var createHandleListboxBlur = function createHandleListboxBlur(otherHandlers) {
    return function (event) {
      var _otherHandlers$onBlur;
      otherHandlers == null ? void 0 : (_otherHandlers$onBlur = otherHandlers.onBlur) == null ? void 0 : _otherHandlers$onBlur.call(otherHandlers, event);
      if (!event.defaultPrevented) {
        onOpenChange == null ? void 0 : onOpenChange(false);
      }
    };
  };
  var listboxReducer = React.useCallback(function (state, action) {
    var newState = defaultListboxReducer(state, action);

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
  var _useButton = useButton({
      disabled: disabled,
      ref: handleButtonRef
    }),
    getButtonRootProps = _useButton.getRootProps,
    buttonActive = _useButton.active,
    buttonFocusVisible = _useButton.focusVisible;
  var optionValues = React.useMemo(function () {
    return options.map(function (o) {
      return o.value;
    });
  }, [options]);
  var useListboxParameters;
  var isOptionDisabled = React.useCallback(function (valueToCheck) {
    var _option$disabled;
    var option = optionsMap.get(valueToCheck);
    return (_option$disabled = option == null ? void 0 : option.disabled) != null ? _option$disabled : false;
  }, [optionsMap]);
  var stringifyOption = React.useCallback(function (valueToCheck) {
    var option = optionsMap.get(valueToCheck);
    if (!option) {
      return '';
    }
    return optionStringifier(option);
  }, [optionsMap, optionStringifier]);
  if (props.multiple) {
    var onChangeMultiple = onChange;
    useListboxParameters = {
      defaultValue: defaultValue,
      id: listboxId,
      isOptionDisabled: isOptionDisabled,
      listboxRef: handleListboxRef,
      multiple: true,
      onChange: function onChange(e, newValues) {
        onChangeMultiple == null ? void 0 : onChangeMultiple(e, newValues);
      },
      onHighlightChange: function onHighlightChange(e, newValue) {
        _onHighlightChange == null ? void 0 : _onHighlightChange(e, newValue != null ? newValue : null);
      },
      options: optionValues,
      optionStringifier: stringifyOption,
      value: valueProp
    };
  } else {
    var onChangeSingle = onChange;
    useListboxParameters = {
      defaultValue: defaultValue,
      id: listboxId,
      isOptionDisabled: isOptionDisabled,
      listboxRef: handleListboxRef,
      multiple: false,
      onChange: function onChange(e, newValue) {
        onChangeSingle == null ? void 0 : onChangeSingle(e, newValue);
      },
      onHighlightChange: function onHighlightChange(e, newValue) {
        _onHighlightChange == null ? void 0 : _onHighlightChange(e, newValue);
      },
      options: optionValues,
      optionStringifier: stringifyOption,
      stateReducer: listboxReducer,
      value: valueProp
    };
  }
  var _useListbox = useListbox(useListboxParameters),
    getListboxRootProps = _useListbox.getRootProps,
    getListboxOptionProps = _useListbox.getOptionProps,
    getOptionState = _useListbox.getOptionState,
    highlightedOption = _useListbox.highlightedOption,
    selectedOption = _useListbox.selectedOption;
  React.useEffect(function () {
    notifySelectionChanged(selectedOption);
  }, [selectedOption, notifySelectionChanged]);
  React.useEffect(function () {
    notifyHighlightChanged(highlightedOption);
  }, [highlightedOption, notifyHighlightChanged]);
  var getButtonProps = function getButtonProps() {
    var otherHandlers = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
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
  var getListboxProps = function getListboxProps() {
    var otherHandlers = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    return getListboxRootProps(_extends({}, otherHandlers, {
      onBlur: createHandleListboxBlur(otherHandlers),
      onKeyUp: createHandleListboxKeyUp(otherHandlers)
    }));
  };
  var getOptionProps = React.useCallback(function (optionValue) {
    var otherHandlers = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
    return getListboxOptionProps(optionValue, _extends({}, otherHandlers, {
      onClick: createHandleListboxItemClick(otherHandlers)
    }));
  }, [getListboxOptionProps, createHandleListboxItemClick]);
  React.useDebugValue({
    selectedOption: selectedOption,
    highlightedOption: highlightedOption,
    open: open
  });
  var contextValue = React.useMemo(function () {
    return {
      listboxRef: listboxRef,
      getOptionProps: getOptionProps,
      getOptionState: getOptionState,
      registerHighlightChangeHandler: registerHighlightChangeHandler,
      registerSelectionChangeHandler: registerSelectionChangeHandler
    };
  }, [getOptionProps, getOptionState, registerHighlightChangeHandler, registerSelectionChangeHandler]);
  return {
    buttonActive: buttonActive,
    buttonFocusVisible: buttonFocusVisible,
    disabled: disabled,
    getButtonProps: getButtonProps,
    getListboxProps: getListboxProps,
    contextValue: contextValue,
    open: open,
    value: selectedOption,
    highlightedOption: highlightedOption
  };
}
export default useSelect;