"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");
Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = useListbox;
var _extends2 = _interopRequireDefault(require("@babel/runtime/helpers/extends"));
var React = _interopRequireWildcard(require("react"));
var _utils = require("@mui/utils");
var _useListbox = require("./useListbox.types");
var _defaultListboxReducer = _interopRequireDefault(require("./defaultListboxReducer"));
var _useControllableReducer = _interopRequireDefault(require("./useControllableReducer"));
var _areArraysEqual = _interopRequireDefault(require("../utils/areArraysEqual"));
var _useLatest = _interopRequireDefault(require("../utils/useLatest"));
var _useTextNavigation = _interopRequireDefault(require("../utils/useTextNavigation"));
function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }
function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }
const defaultOptionComparer = (optionA, optionB) => optionA === optionB;
const defaultIsOptionDisabled = () => false;
const defaultOptionStringifier = option => typeof option === 'string' ? option : String(option);

/**
 * @ignore - do not document.
 */
function useListbox(props) {
  var _props$optionIdGenera;
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
  const id = (0, _utils.unstable_useId)(idProp);
  const defaultIdGenerator = React.useCallback((_, index) => `${id}-option-${index}`, [id]);
  const optionIdGenerator = (_props$optionIdGenera = props.optionIdGenerator) != null ? _props$optionIdGenera : defaultIdGenerator;
  const propsWithDefaults = (0, _useLatest.default)((0, _extends2.default)({}, props, {
    disabledItemsFocusable,
    disableListWrap,
    focusManagement,
    isOptionDisabled,
    multiple,
    optionComparer,
    optionStringifier
  }), [props]);
  const listboxRef = React.useRef(null);
  const handleRef = (0, _utils.unstable_useForkRef)(externalListboxRef, listboxRef);
  const [{
    highlightedValue,
    selectedValue
  }, dispatch] = (0, _useControllableReducer.default)(_defaultListboxReducer.default, externalReducer, propsWithDefaults);
  const handleTextNavigation = (0, _useTextNavigation.default)((searchString, event) => dispatch({
    type: _useListbox.ActionTypes.textNavigation,
    event,
    searchString
  }));
  React.useEffect(() => {
    // if a controlled value changes, we need to update the state to keep things in sync
    if (valueParam !== undefined && valueParam !== selectedValue) {
      dispatch({
        type: _useListbox.ActionTypes.setValue,
        event: null,
        value: valueParam
      });
    }
  }, [valueParam, selectedValue, dispatch]);
  const highlightedIndex = React.useMemo(() => {
    return highlightedValue == null ? -1 : options.findIndex(option => optionComparer(option, highlightedValue));
  }, [highlightedValue, options, optionComparer]);

  // introducing refs to avoid recreating the getOptionState function on each change.
  const latestSelectedValue = (0, _useLatest.default)(selectedValue);
  const latestHighlightedIndex = (0, _useLatest.default)(highlightedIndex);
  const previousOptions = React.useRef([]);
  React.useEffect(() => {
    if ((0, _areArraysEqual.default)(previousOptions.current, options, optionComparer)) {
      return;
    }
    dispatch({
      type: _useListbox.ActionTypes.optionsChange,
      event: null,
      options,
      previousOptions: previousOptions.current
    });
    previousOptions.current = options;
  }, [options, optionComparer, dispatch]);
  const setSelectedValue = React.useCallback(option => {
    dispatch({
      type: _useListbox.ActionTypes.setValue,
      event: null,
      value: option
    });
  }, [dispatch]);
  const setHighlightedValue = React.useCallback(option => {
    dispatch({
      type: _useListbox.ActionTypes.setHighlight,
      event: null,
      highlight: option
    });
  }, [dispatch]);
  const createHandleOptionClick = React.useCallback((option, other) => event => {
    var _other$onClick;
    (_other$onClick = other.onClick) == null ? void 0 : _other$onClick.call(other, event);
    if (event.defaultPrevented) {
      return;
    }
    event.preventDefault();
    dispatch({
      type: _useListbox.ActionTypes.optionClick,
      option,
      event
    });
  }, [dispatch]);
  const createHandleOptionPointerOver = React.useCallback((option, other) => event => {
    var _other$onMouseOver;
    (_other$onMouseOver = other.onMouseOver) == null ? void 0 : _other$onMouseOver.call(other, event);
    if (event.defaultPrevented) {
      return;
    }
    dispatch({
      type: _useListbox.ActionTypes.optionHover,
      option,
      event
    });
  }, [dispatch]);
  const createHandleKeyDown = other => event => {
    var _other$onKeyDown;
    (_other$onKeyDown = other.onKeyDown) == null ? void 0 : _other$onKeyDown.call(other, event);
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
      type: _useListbox.ActionTypes.keyDown,
      event
    });
    handleTextNavigation(event);
  };
  const createHandleBlur = other => event => {
    var _other$onBlur, _listboxRef$current;
    (_other$onBlur = other.onBlur) == null ? void 0 : _other$onBlur.call(other, event);
    if (event.defaultPrevented) {
      return;
    }
    if ((_listboxRef$current = listboxRef.current) != null && _listboxRef$current.contains(document.activeElement)) {
      // focus is within the listbox
      return;
    }
    dispatch({
      type: _useListbox.ActionTypes.blur,
      event
    });
  };
  const getRootProps = (otherHandlers = {}) => {
    return (0, _extends2.default)({}, otherHandlers, {
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
      var _ref;
      selected = ((_ref = latestSelectedValue.current) != null ? _ref : []).some(value => value != null && optionComparer(option, value));
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
    return (0, _extends2.default)({}, otherHandlers, {
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