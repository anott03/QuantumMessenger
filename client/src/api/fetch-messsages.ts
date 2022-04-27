function useFetchMessages(): (userId: String) => Promise<Object> {
  return async function(userId: String) {
    const URI = "http://localhost:8000/v1/fetch-messages";
    const opts: RequestInit = {
      method: "POST", 
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin':'*',
        'Content-Type':'application/json'
      },

      body: JSON.stringify({
        username: "test",
        receiver_id: userId,
      })
    }

    let data = await fetch(URI, opts).then(res => res.json()).then(data => {
      return data;
    }).catch(err => {
      console.error(err);
    })

    return data;
  }
}

export { useFetchMessages }
