import './Register.css'
import { Link } from 'react-router-dom';

export default function Register() {
  return (
      <div className='register'>
          <div className='registerWrapper'>
              <div className="registerBox">
                  <input placeholder='Username' className='registerInput' />
                  <input type="email" id="email" size="30" placeholder="e-mail address"  className='registerInput'/>
                  <input type="password" placeholder="Password"  className='registerInput' />
                  <input type="password" placeholder="Confirm Password"  className='registerInput'/>
                  <button className='registerButton'>Register</button>
                  <div className="registerFooter">
                      <span className="registerText">Already have an account?</span>
                      <Link to="/login"><button className="registerLoginButton">Log In</button></Link>
                  </div>
              </div>
          </div>  
    </div>
  )
}
