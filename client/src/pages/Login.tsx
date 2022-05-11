import './styles/Login.css';
import { useAppDispatch } from '../redux/hooks';
import { setUser } from '../redux/reducers/userSlice';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const onSubmit: React.FormEventHandler = (e: any) => {
    e.preventDefault();

    let username: String = e.target["username"].value;
    dispatch(setUser({ username }));
    navigate("/home");
  }

  return (
    <div className="login">
      <div className="login-content">
        <h1>Login</h1>
        <form onSubmit={onSubmit}>
          <input id="username" type="text" placeholder="Username" />
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

export default Login;
