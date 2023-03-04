import _slicedToArray from "@babel/runtime/helpers/esm/slicedToArray";
import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";
import _typeof from "@babel/runtime/helpers/esm/typeof";
import _extends from "@babel/runtime/helpers/esm/extends";
function isNestedContainer(ownerState) {
  return ownerState.level > 0 && ownerState.container;
}
function createGetSelfSpacing(ownerState) {
  return function getSelfSpacing(axis) {
    return "var(--Grid-".concat(axis, "Spacing").concat(ownerState.level || '', ")");
  };
}
function createGetParentSpacing(ownerState) {
  return function getParentSpacing(axis) {
    if (ownerState.level === 0) {
      return "var(--Grid-".concat(axis, "Spacing)");
    }
    return "var(--Grid-".concat(axis, "Spacing").concat(ownerState.level - 1 || '', ")");
  };
}
export var filterBreakpointKeys = function filterBreakpointKeys(breakpointsKeys, responsiveKeys) {
  return breakpointsKeys.filter(function (key) {
    return responsiveKeys.includes(key);
  });
};
export var traverseBreakpoints = function traverseBreakpoints(breakpoints, responsive, iterator) {
  var smallestBreakpoint = breakpoints.keys[0]; // the keys is sorted from smallest to largest by `createBreakpoints`.

  if (Array.isArray(responsive)) {
    responsive.forEach(function (breakpointValue, index) {
      iterator(function (responsiveStyles, style) {
        if (index <= breakpoints.keys.length - 1) {
          if (index === 0) {
            _extends(responsiveStyles, style);
          } else {
            responsiveStyles[breakpoints.up(breakpoints.keys[index])] = style;
          }
        }
      }, breakpointValue);
    });
  } else if (responsive && _typeof(responsive) === 'object') {
    // prevent null
    // responsive could be a very big object, pick the smallest responsive values

    var keys = Object.keys(responsive).length > breakpoints.keys.length ? breakpoints.keys : filterBreakpointKeys(breakpoints.keys, Object.keys(responsive));
    keys.forEach(function (key) {
      if (breakpoints.keys.indexOf(key) !== -1) {
        // @ts-ignore already checked that responsive is an object
        var breakpointValue = responsive[key];
        if (breakpointValue !== undefined) {
          iterator(function (responsiveStyles, style) {
            if (smallestBreakpoint === key) {
              _extends(responsiveStyles, style);
            } else {
              responsiveStyles[breakpoints.up(key)] = style;
            }
          }, breakpointValue);
        }
      }
    });
  } else if (typeof responsive === 'number' || typeof responsive === 'string') {
    iterator(function (responsiveStyles, style) {
      _extends(responsiveStyles, style);
    }, responsive);
  }
};
export var generateGridSizeStyles = function generateGridSizeStyles(_ref) {
  var theme = _ref.theme,
    ownerState = _ref.ownerState;
  var getSelfSpacing = createGetSelfSpacing(ownerState);
  var styles = {};
  traverseBreakpoints(theme.breakpoints, ownerState.gridSize, function (appendStyle, value) {
    var style = {};
    if (value === true) {
      style = {
        flexBasis: 0,
        flexGrow: 1,
        maxWidth: '100%'
      };
    }
    if (value === 'auto') {
      style = {
        flexBasis: 'auto',
        flexGrow: 0,
        flexShrink: 0,
        maxWidth: 'none',
        width: 'auto'
      };
    }
    if (typeof value === 'number') {
      style = {
        flexGrow: 0,
        flexBasis: 'auto',
        width: "calc(100% * ".concat(value, " / var(--Grid-columns)").concat(isNestedContainer(ownerState) ? " + ".concat(getSelfSpacing('column')) : '', ")")
      };
    }
    appendStyle(styles, style);
  });
  return styles;
};
export var generateGridOffsetStyles = function generateGridOffsetStyles(_ref2) {
  var theme = _ref2.theme,
    ownerState = _ref2.ownerState;
  var styles = {};
  traverseBreakpoints(theme.breakpoints, ownerState.gridOffset, function (appendStyle, value) {
    var style = {};
    if (value === 'auto') {
      style = {
        marginLeft: 'auto'
      };
    }
    if (typeof value === 'number') {
      style = {
        marginLeft: value === 0 ? '0px' : "calc(100% * ".concat(value, " / var(--Grid-columns))")
      };
    }
    appendStyle(styles, style);
  });
  return styles;
};
export var generateGridColumnsStyles = function generateGridColumnsStyles(_ref3) {
  var theme = _ref3.theme,
    ownerState = _ref3.ownerState;
  if (!ownerState.container) {
    return {};
  }
  var styles = {
    '--Grid-columns': 12
  };
  traverseBreakpoints(theme.breakpoints, ownerState.columns, function (appendStyle, value) {
    appendStyle(styles, {
      '--Grid-columns': value
    });
  });
  return styles;
};
export var generateGridRowSpacingStyles = function generateGridRowSpacingStyles(_ref4) {
  var theme = _ref4.theme,
    ownerState = _ref4.ownerState;
  if (!ownerState.container) {
    return {};
  }
  var getParentSpacing = createGetParentSpacing(ownerState);
  var styles = isNestedContainer(ownerState) ? _defineProperty({}, "--Grid-rowSpacing".concat(ownerState.level || ''), getParentSpacing('row')) : {};
  traverseBreakpoints(theme.breakpoints, ownerState.rowSpacing, function (appendStyle, value) {
    var _theme$spacing;
    appendStyle(styles, _defineProperty({}, "--Grid-rowSpacing".concat(ownerState.level || ''), typeof value === 'string' ? value : (_theme$spacing = theme.spacing) == null ? void 0 : _theme$spacing.call(theme, value)));
  });
  return styles;
};
export var generateGridColumnSpacingStyles = function generateGridColumnSpacingStyles(_ref6) {
  var theme = _ref6.theme,
    ownerState = _ref6.ownerState;
  if (!ownerState.container) {
    return {};
  }
  var getParentSpacing = createGetParentSpacing(ownerState);
  var styles = isNestedContainer(ownerState) ? _defineProperty({}, "--Grid-columnSpacing".concat(ownerState.level || ''), getParentSpacing('column')) : {};
  traverseBreakpoints(theme.breakpoints, ownerState.columnSpacing, function (appendStyle, value) {
    var _theme$spacing2;
    appendStyle(styles, _defineProperty({}, "--Grid-columnSpacing".concat(ownerState.level || ''), typeof value === 'string' ? value : (_theme$spacing2 = theme.spacing) == null ? void 0 : _theme$spacing2.call(theme, value)));
  });
  return styles;
};
export var generateGridDirectionStyles = function generateGridDirectionStyles(_ref8) {
  var theme = _ref8.theme,
    ownerState = _ref8.ownerState;
  if (!ownerState.container) {
    return {};
  }
  var styles = {};
  traverseBreakpoints(theme.breakpoints, ownerState.direction, function (appendStyle, value) {
    appendStyle(styles, {
      flexDirection: value
    });
  });
  return styles;
};
export var generateGridStyles = function generateGridStyles(_ref9) {
  var ownerState = _ref9.ownerState;
  var getSelfSpacing = createGetSelfSpacing(ownerState);
  var getParentSpacing = createGetParentSpacing(ownerState);
  return _extends({
    minWidth: 0,
    boxSizing: 'border-box'
  }, ownerState.container && _extends({
    display: 'flex',
    flexWrap: 'wrap'
  }, ownerState.wrap && ownerState.wrap !== 'wrap' && {
    flexWrap: ownerState.wrap
  }, {
    margin: "calc(".concat(getSelfSpacing('row'), " / -2) calc(").concat(getSelfSpacing('column'), " / -2)")
  }, ownerState.disableEqualOverflow && {
    margin: "calc(".concat(getSelfSpacing('row'), " * -1) 0px 0px calc(").concat(getSelfSpacing('column'), " * -1)")
  }), (!ownerState.container || isNestedContainer(ownerState)) && _extends({
    padding: "calc(".concat(getParentSpacing('row'), " / 2) calc(").concat(getParentSpacing('column'), " / 2)")
  }, (ownerState.disableEqualOverflow || ownerState.parentDisableEqualOverflow) && {
    padding: "".concat(getParentSpacing('row'), " 0px 0px ").concat(getParentSpacing('column'))
  }));
};
export var generateSizeClassNames = function generateSizeClassNames(gridSize) {
  var classNames = [];
  Object.entries(gridSize).forEach(function (_ref10) {
    var _ref11 = _slicedToArray(_ref10, 2),
      key = _ref11[0],
      value = _ref11[1];
    if (value !== false && value !== undefined) {
      classNames.push("grid-".concat(key, "-").concat(String(value)));
    }
  });
  return classNames;
};
export var generateSpacingClassNames = function generateSpacingClassNames(spacing) {
  var smallestBreakpoint = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'xs';
  function isValidSpacing(val) {
    if (val === undefined) {
      return false;
    }
    return typeof val === 'string' && !Number.isNaN(Number(val)) || typeof val === 'number' && val > 0;
  }
  if (isValidSpacing(spacing)) {
    return ["spacing-".concat(smallestBreakpoint, "-").concat(String(spacing))];
  }
  if (_typeof(spacing) === 'object' && !Array.isArray(spacing)) {
    var classNames = [];
    Object.entries(spacing).forEach(function (_ref12) {
      var _ref13 = _slicedToArray(_ref12, 2),
        key = _ref13[0],
        value = _ref13[1];
      if (isValidSpacing(value)) {
        classNames.push("spacing-".concat(key, "-").concat(String(value)));
      }
    });
    return classNames;
  }
  return [];
};
export var generateDirectionClasses = function generateDirectionClasses(direction) {
  if (direction === undefined) {
    return [];
  }
  if (_typeof(direction) === 'object') {
    return Object.entries(direction).map(function (_ref14) {
      var _ref15 = _slicedToArray(_ref14, 2),
        key = _ref15[0],
        value = _ref15[1];
      return "direction-".concat(key, "-").concat(value);
    });
  }
  return ["direction-xs-".concat(String(direction))];
};