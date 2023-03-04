"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");
Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = useOption;
var _extends2 = _interopRequireDefault(require("@babel/runtime/helpers/extends"));
var React = _interopRequireWildcard(require("react"));
var _utils = require("@mui/utils");
var _SelectUnstyledContext = require("../SelectUnstyled/SelectUnstyledContext");
var _useForcedRerendering = _interopRequireDefault(require("../utils/useForcedRerendering"));
function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }
function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }
/**
 *
 * API:
 *
 * - [useOption API](https://mui.com/base/api/use-option/)
 */
function useOption(params) {
  const {
    value,
    optionRef: optionRefParam
  } = params;
  const selectContext = React.useContext(_SelectUnstyledContext.SelectUnstyledContext);
  if (!selectContext) {
    throw new Error('Option must have access to the SelectUnstyledContext (i.e., be used inside a SelectUnstyled component).');
  }
  const {
    getOptionProps,
    getOptionState,
    listboxRef,
    registerHighlightChangeHandler,
    registerSelectionChangeHandler
  } = selectContext;
  const optionState = getOptionState(value);
  const {
    selected,
    highlighted
  } = optionState;
  const rerender = (0, _useForcedRerendering.default)();
  React.useEffect(() => {
    function updateSelectedState(selectedValues) {
      if (!selected) {
        if (Array.isArray(selectedValues)) {
          if (selectedValues.includes(value)) {
            rerender();
          }
        } else if (selectedValues === value) {
          rerender();
        }
      } else if (Array.isArray(selectedValues)) {
        if (!selectedValues.includes(value)) {
          rerender();
        }
      } else if (selectedValues !== value) {
        rerender();
      }
    }
    return registerSelectionChangeHandler(updateSelectedState);
  }, [registerSelectionChangeHandler, rerender, selected, value]);
  React.useEffect(() => {
    function updateHighlightedState(highlightedValue) {
      if (highlightedValue === value && !highlighted) {
        rerender();
      } else if (highlightedValue !== value && highlighted) {
        rerender();
      }
    }
    return registerHighlightChangeHandler(updateHighlightedState);
  }, [registerHighlightChangeHandler, rerender, value, highlighted]);
  const optionRef = React.useRef(null);
  const handleRef = (0, _utils.unstable_useForkRef)(optionRefParam, optionRef);
  React.useEffect(() => {
    // Scroll to the currently highlighted option
    if (highlighted) {
      if (!listboxRef.current || !optionRef.current) {
        return;
      }
      const listboxClientRect = listboxRef.current.getBoundingClientRect();
      const optionClientRect = optionRef.current.getBoundingClientRect();
      if (optionClientRect.top < listboxClientRect.top) {
        listboxRef.current.scrollTop -= listboxClientRect.top - optionClientRect.top;
      } else if (optionClientRect.bottom > listboxClientRect.bottom) {
        listboxRef.current.scrollTop += optionClientRect.bottom - listboxClientRect.bottom;
      }
    }
  }, [highlighted, listboxRef]);
  return {
    getRootProps: (otherHandlers = {}) => (0, _extends2.default)({}, otherHandlers, getOptionProps(value, otherHandlers), {
      ref: handleRef
    }),
    highlighted,
    index: optionState.index,
    selected
  };
}