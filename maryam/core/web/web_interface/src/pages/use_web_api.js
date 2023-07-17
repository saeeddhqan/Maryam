import { useState, useEffect } from "react";

const useWebApi = (term) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    let timer;

    setIsLoading(true);

    const fetchData = async () => {
      await fetch(
        `http://127.0.0.1:1313/api/modules?_module=iris&query=${term}`
      )
        .then((response) => response.json())
        .then((result) => {
          setData(result);
        })
        .catch((error) => {
          console.log(error);
        })
        .finally(() => {
          timer = setTimeout(() => {
            setIsLoading(false);
          }, 7000);
        });
    };

    fetchData();

    return () => clearTimeout(timer);
  }, [term]);

  return { data, isLoading };
};

export default useWebApi;
