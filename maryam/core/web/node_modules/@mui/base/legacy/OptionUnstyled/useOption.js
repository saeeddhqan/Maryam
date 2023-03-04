import _extends from "@babel/runtime/helpers/esm/extends";
import * as React from 'react';
import { unstable_useForkRef as useForkRef } from '@mui/utils';
import { SelectUnstyledContext } from '../SelectUnstyled/SelectUnstyledContext';
import useForcedRerendering from '../utils/useForcedRerendering';

/**
 *
 * API:
 *
 * - [useOption API](https://mui.com/base/api/use-option/)
 */
export default function useOption(params) {
  var value = params.value,
    optionRefParam = params.optionRef;
  var selectContext = React.useContext(SelectUnstyledContext);
  if (!selectContext) {
    throw new Error('Option must have access to the SelectUnstyledContext (i.e., be used inside a SelectUnstyled component).');
  }
  var getOptionProps = selectContext.getOptionProps,
    getOptionState = selectContext.getOptionState,
    listboxRef = selectContext.listboxRef,
    registerHighlightChangeHandler = selectContext.registerHighlightChangeHandler,
    registerSelectionChangeHandler = selectContext.registerSelectionChangeHandler;
  var optionState = getOptionState(value);
  var selected = optionState.selected,
    highlighted = optionState.highlighted;
  var rerender = useForcedRerendering();
  React.useEffect(function () {
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
  React.useEffect(function () {
    function updateHighlightedState(highlightedValue) {
      if (highlightedValue === value && !highlighted) {
        rerender();
      } else if (highlightedValue !== value && highlighted) {
        rerender();
      }
    }
    return registerHighlightChangeHandler(updateHighlightedState);
  }, [registerHighlightChangeHandler, rerender, value, highlighted]);
  var optionRef = React.useRef(null);
  var handleRef = useForkRef(optionRefParam, optionRef);
  React.useEffect(function () {
    // Scroll to the currently highlighted option
    if (highlighted) {
      if (!listboxRef.current || !optionRef.current) {
        return;
      }
      var listboxClientRect = listboxRef.current.getBoundingClientRect();
      var optionClientRect = optionRef.current.getBoundingClientRect();
      if (optionClientRect.top < listboxClientRect.top) {
        listboxRef.current.scrollTop -= listboxClientRect.top - optionClientRect.top;
      } else if (optionClientRect.bottom > listboxClientRect.bottom) {
        listboxRef.current.scrollTop += optionClientRect.bottom - listboxClientRect.bottom;
      }
    }
  }, [highlighted, listboxRef]);
  return {
    getRootProps: function getRootProps() {
      var otherHandlers = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      return _extends({}, otherHandlers, getOptionProps(value, otherHandlers), {
        ref: handleRef
      });
    },
    highlighted: highlighted,
    index: optionState.index,
    selected: selected
  };
}