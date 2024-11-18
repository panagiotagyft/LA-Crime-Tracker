import './Login.css'
import { Link } from 'react-router-dom';

export default function Login() {
  return (
      <div className='login'>
          <div className='loginWrapper'>
              <div className="loginBox">
                  <input placeholder='Username' className='loginInput' />
                  <input type="password" placeholder="Password"  className='loginInput' />
                  <button className='loginButton'>Log In</button>
                  <div className="loginFooter">
                      <span className="loginText">Don't have an account?</span>
                      <Link to="/register">
                          <button className="loginRegisterButton">Sign Up</button>
                      </Link>
                  </div>
              </div>
          </div>  
    </div>
  )
}
