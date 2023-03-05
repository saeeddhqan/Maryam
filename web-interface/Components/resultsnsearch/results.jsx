export default function Results({ data, LowerLimit, UpperLimit }) {
  const arr1 = data.slice(LowerLimit, UpperLimit);
  return arr1.map((item) => {
    return (
      <div className="results">
        <p className="route">{item.c}</p>
        <a className="link" href={item.a}>
          {item.t}
        </a>
        <p className="info">{item.d}</p>
      </div>
    );
  });
}
