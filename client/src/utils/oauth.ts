import { useAppDispatch } from "../redux/hooks";
import { setUser } from "../redux/reducers/userSlice";
import { getAuth, signInWithPopup, GithubAuthProvider, GoogleAuthProvider } from 'firebase/auth';
import { useNavigate } from 'react-router-dom';

function useOAuth(): { githubOAuth: () => void, googleOAuth: () => void } {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  function oauth(provider: any) {
      const auth = getAuth();
      signInWithPopup(auth, provider)
        .then((result: any) => {
          // Github Access Tokens if we need to access the github API
          // const credential = GithubAuthProvider.credentialFromResult(result);
          // const token = credential.accessToken;
          const user = result.user;
          console.log(user)
          dispatch(setUser({
            email: user.email,
            displayName: user.displayName,
          }));
          navigate("/home");
        })
        .catch((error: any) => console.error(error));
  }

  return {
    githubOAuth: () => {
      const provider = new GithubAuthProvider();
      oauth(provider);
    },
    googleOAuth: () => {
      const provider = new GoogleAuthProvider();
      oauth(provider);
    }
  }
}

export default useOAuth;
