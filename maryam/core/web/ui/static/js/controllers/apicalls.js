import { createResult } from "./createResult.js";

export function searchInIris(query) {
    fetch("http://127.0.0.1:1313/api/modules?_module=iris&query="+query)
        .then(res => res.json())
        .then((data)=>createResult(query, data))
        .catch((err) => {
            alert("Failed to connect with the API, kindly check the backend service");
            console.log(err);
        })
}



