import { Buffer } from 'buffer';

function useSendMessage(): (messageId: String, message: String) => void {
  return async function(messageId: String, message: String) {
    const URI = "http://localhost:8000/v1/send-message";
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
        message_content: message
      })
    }

    await fetch(URI, opts).then(res => res.json()).then(res => {
      console.log(res);
    }).catch(err => {
      console.error(err);
    })
  }
}

export { useSendMessage }
