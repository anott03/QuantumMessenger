import './styles/Login.css';
import useOAuth from '../utils/oauth';

const Login = () => {
  const oauth = useOAuth();

  return (
    <div className="login">
      <div className="login-content">
        <h1>Login</h1>
        <button onClick={oauth}>Login with GitHub</button>
      </div>
    </div>
  );
}

export default Login;
