function useQuantumKeyGen() {
    const URI = "http://localhost:8000/api/v1/qc/generate-key";
    const opts = { method: "GET" };
    fetch(URI, opts).then(res => res.json()).then(data => {
        console.log(data);
    })
}

export { useQuantumKeyGen }
