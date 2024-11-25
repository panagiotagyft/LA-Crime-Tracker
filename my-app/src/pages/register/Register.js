import "./Register.css";
import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

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
    const { name, value } = event.target;
    setInputs((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/api/users/add_user", inputs, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      redirect("/"); // Redirect to the homepage
    } catch (error) {
      console.error("Error details:", error);
      if (error.response) {
        const errorData = error.response.data.errors;
        let errorMessage = "";
        for (const key in errorData) {
          if (errorData.hasOwnProperty(key)) {
            errorMessage += `${key}: ${errorData[key].join(", ")} `;
          }
        }
        setError(errorMessage.trim());
      } else {
        setError("An unexpected error occurred. Please try again later.");
      }
    }
  };

  return (
    <div className="register">
      <div className="registerWrapper">
        <div className="registerBox">
          <form onSubmit={handleSubmit}>
            <input
              name="username"
              placeholder="Username"
              className="registerInput"
              onChange={handleChange}
            />
            <input
              name="email"
              type="email"
              placeholder="e-mail address"
              className="registerInput"
              onChange={handleChange}
            />
            <input
              name="password"
              type="password"
              placeholder="Password"
              className="registerInput"
              onChange={handleChange}
            />
            <input
              name="confirm_password"
              type="password"
              placeholder="Confirm Password"
              className="registerInput"
              onChange={handleChange}
            />

            {error && <div className="error">{error}</div>}
            <button className="registerButton" type="submit">
              Register
            </button>
          </form>
          <div className="registerFooter">
            <span className="registerText">Already have an account?</span>
            <Link to="/login">
              <button className="registerLoginButton">Log In</button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
