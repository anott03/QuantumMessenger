import './styles/Login.css';

const Login = () => {
  return (
    <div className="login">
      <div className="login-content">
        <h1>Login</h1>
        <form>
          <input type="text" placeholder="Username" />
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

export default Login;
