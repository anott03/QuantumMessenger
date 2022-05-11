import { useAppDispatch } from "../redux/hooks";
import { setMessages } from "../redux/reducers/userSlice";

function useFetchMessages(): (userId: String) => Promise<void> {
  const dispatch = useAppDispatch();

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
      console.log(data);
      dispatch(setMessages(data));
    }).catch(err => {
      console.error(err);
    })
  }
}

export { useFetchMessages }
