import { Buffer } from 'buffer';

function useFetchKey(): (messageId: String) => Promise<Buffer> {
  return async function(messageId: String) {
    const URI = "http://localhost:8000/v1/qc/fetch-key";
    const opts: RequestInit = {
      method: "POST", 
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin':'*',
        'Content-Type':'application/json'
      },

      body: JSON.stringify({
        message_id: messageId,
      })
    }

    let key = await fetch(URI, opts).then(res => res.json()).then(data => {
      return data["key"];
    }).catch(err => {
      console.error(err);
    })

    return Buffer.alloc(key.length, key);
  }
}

export { useFetchKey }
