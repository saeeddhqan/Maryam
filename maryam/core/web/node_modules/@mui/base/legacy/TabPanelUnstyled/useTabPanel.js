import { useTabContext, getPanelId, getTabId } from '../TabsUnstyled';
/**
 *
 * Demos:
 *
 * - [Unstyled Tabs](https://mui.com/base/react-tabs/#hooks)
 *
 * API:
 *
 * - [useTabPanel API](https://mui.com/base/api/use-tab-panel/)
 */
function useTabPanel(parameters) {
  var value = parameters.value;
  var context = useTabContext();
  if (context === null) {
    throw new Error('No TabContext provided');
  }
  var hidden = value !== context.value;
  var id = getPanelId(context, value);
  var tabId = getTabId(context, value);
  var getRootProps = function getRootProps() {
    return {
      'aria-labelledby': tabId != null ? tabId : undefined,
      hidden: hidden,
      id: id != null ? id : undefined
    };
  };
  return {
    hidden: hidden,
    getRootProps: getRootProps
  };
}
export default useTabPanel;