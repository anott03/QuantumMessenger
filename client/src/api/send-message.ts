import { Buffer } from 'buffer';
import { useAppSelector } from "../redux/hooks";
import { selectUser } from "../redux/reducers/userSlice";

function useSendMessage(): (messageId: String, message: String, receiver: String) => void {
  const user = useAppSelector(selectUser)
  return async function(messageId: String, message: String, receiver: String) {
    const URI = "http://localhost:8000/v1/send-message";
    const opts: RequestInit = {
      method: "POST", 
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin':'*',
        'Content-Type':'application/json'
      },

      body: JSON.stringify({
        sender_id: user.username,
        receiver_id: receiver,
        message_id: messageId,
        message_content: message,
        timestamp: Date.now().toString()
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
