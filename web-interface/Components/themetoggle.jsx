export default function Themetoggle({ theme, setTheme }) {
  const toggleTheme = () => {
    if (theme == "light") {
      setTheme("dark");
    } else {
      setTheme("light");
    }
  };
  return (
    <div className="theme-toggle">
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
}
