import { useAppDispatch, useAppSelector } from "../redux/hooks";
import { setMessages, selectUser } from "../redux/reducers/userSlice";
import { useFetchKey } from "../api/fetch-key";

function useFetchMessages(): (userId: String) => Promise<void> {
  const dispatch = useAppDispatch();
  const user = useAppSelector(selectUser);
  const fetchKey = useFetchKey()

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
        username: user.username,
        receiver_id: userId,
      })
    }

    let data = await fetch(URI, opts).then(res => res.json()).then(data => {
      console.log(data);
      // @ts-ignore
      let newData = []
      for (const message of data) {
        console.log("message", message)
        // @ts-ignore
        let keyStr = message.key
        console.log("key str", keyStr)
        // @ts-ignore
        let content = message["content"]
        let decryptedBytes = ""
        let keyPointer = 0
        for (let i = 0; i < content.length; i++) {
          let messageBit = Number.parseInt(content[i])
          let keyBit = Number.parseInt(keyStr[keyPointer])
          decryptedBytes += messageBit === keyBit ? "0" : "1"
          keyPointer += 1
          keyPointer %= keyStr.length
        }
        let reconstructed = ""
        for (let i = 0; i < decryptedBytes.length; i+=7) {
          let chunk = decryptedBytes.slice(i, i+7)
          reconstructed += String.fromCharCode(Number.parseInt(chunk, 2))
        }
        // @ts-ignore
        let newMessage = {message_id: message["message_id"], sender: message["sender"], content: reconstructed}
        newData.push(newMessage)
      }
      // @ts-ignore
      dispatch(setMessages(newData));
    }).catch(err => {
      console.error(err);
    })
  }
}

export { useFetchMessages }
