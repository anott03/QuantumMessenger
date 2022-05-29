import { setInteractingUsers } from "../redux/reducers/userSlice";
import { useAppDispatch } from "../redux/hooks";

function useInteractingUsers(): (username: String) => Promise<void> {
    const dispatch = useAppDispatch()

    return async function(username: String) {
        const URI = `${process.env.REACT_APP_API_ROOT}interacting-users`;
        const opts: RequestInit = {
            method: "POST",
            mode: 'cors',
            headers: {
                'Access-Control-Allow-Origin':'*',
                'Content-Type':'application/json'
            },

            body: JSON.stringify({
                username: username,
            })
        }

        let data = await fetch(URI, opts).then(res => res.json()).then(data => {
            console.log("interacting users", data)
            dispatch(setInteractingUsers(data["users"]))
        }).catch(err => {
            console.error(err);
        })
    }
}

export { useInteractingUsers }
