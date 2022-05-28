import { Buffer } from 'buffer';

function useQuantumKeyGen(): (messageId: String) => Promise<String> {
  return async function(messageId: String) {
    const URI = `${process.env.REACT_APP_API_ROOT}generate-key`;
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
      return data;
    }).catch(err => {
      console.error(err);
    })

    return key["key"]
  }
}

export { useQuantumKeyGen }
