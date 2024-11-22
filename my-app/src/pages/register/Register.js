import './Register.css'
import { useState } from "react";
import axios from "axios";
import { Link } from 'react-router-dom';

export default function Register() {
    const [error, setError] = useState(null);
    const [inputs, setInputs] = useState({
        username: "",
        email: "",
        password: "",
        confirm_password: "",
    });
    const redirect = useNavigate();

    const handleChange = (event) => {
        let value = event.target.value;
        let name = event.target.name;
        setInputs((prev) => {
            return {
                ...prev,
                [name]: value || null,
            };
        });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const params = new URLSearchParams();
        Object.keys(inputs).forEach((key) => {
            params.append(key, inputs[key]);
        });

        try {
            await axios.post("https://127.0.0.1/register-app/signup/", params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
            redirect("/");
        } catch (error) {
            console.error("Error details:", error);
            if (error.response) {
                // Extracting error message
                const errorData = error.response.data.errors;
                let errorMessage = "";
                for (const key in errorData) {
                    if (errorData.hasOwnProperty(key)) {
                        errorMessage += `${key}: ${errorData[key].join(", ")} `;
                    }
                }
                setError(errorMessage.trim()); // Set formatted error message
            } else {
                // Handle errors that don't have a response (e.g., network issues)
                setError("An unexpected error occurred. Please try again later.");
            }
        }
    };

    return (
        <div className='register'>
            <div className='registerWrapper'>
                <div className="registerBox" onSubmit={handleSubmit}>
                    <input placeholder='Username' className='registerInput' />
                    <input type="email" id="email" size="30" placeholder="e-mail address"  className='registerInput'/>
                    <input type="password" placeholder="Password"  className='registerInput' />
                    <input type="password" placeholder="Confirm Password" className='registerInput' />
                    
                    {error && <div className="error">{error}</div>}
                    <button className='registerButton' onClick={handleSubmit}>Register</button>
                    <div className="registerFooter">
                        <span className="registerText">Already have an account?</span>
                        <Link to="/login"><button className="registerLoginButton">Log In</button></Link>
                    </div>
                </div>
            </div>  
        </div>
    )
}
