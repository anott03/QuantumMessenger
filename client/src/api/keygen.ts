import { Buffer } from 'buffer';

function useQuantumKeyGen(): (messageId: String) => Promise<Buffer> {
  return async function(messageId: String) {
    const URI = "http://localhost:8000/v1/qc/generate-key";
    const opts: RequestInit = {
      method: "POST", 
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin':'*',
        'Content-Type':'application/json'
      },

      body: JSON.stringify({
        username: "test",
        user_id: "test",
        receiver_id: "test2",
        message_id: messageId,
      })
    }

    let key = await fetch(URI, opts).then(res => res.json()).then(data => {
      return data;
    }).catch(err => {
      console.error(err);
    })

    return Buffer.alloc(key.length, key);
  }
}

export { useQuantumKeyGen }
