import { useState } from "react";
import Navbar from "./Navbar";
import "./Login.css";

function Login() {
  const [credentials, setCredentials] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({
    email: "",
    password: "",
    general: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials({ ...credentials, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    let newErrors = {};

    // Validation checks
    if (credentials.email === "" || credentials.password === "") {
      newErrors.general = "Please fill in all fields.";
      setErrors(newErrors);
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(credentials.email)) {
      newErrors.email = "Please enter a valid email address.";
      setErrors(newErrors);
      return;
    }

    setErrors({});

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/users/login", // ✅ correct endpoint
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include", // ✅ keep Flask-Login cookies
          body: JSON.stringify(credentials),
        }
      );

      const data = await response.json();

      if (response.ok) {
        console.log("Login successful!");
        console.log(data);
      } else {
        console.log("Login failed:", data.error || data.message);
      }
    } catch (error) {
      console.error("Error connecting to server:", error);
    }
  };

  return (
    <div className="login">
      <Navbar />
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <label>Email</label>
        <input
          type="email"
          name="email"
          placeholder="Enter your Email Address"
          required
          value={credentials.email}
          onChange={handleChange}
        />
        {errors.email && <p className="error-text">{errors.email}</p>}

        <label>Password</label>
        <input
          type="password"
          name="password"
          placeholder="Enter your Password"
          required
          value={credentials.password}
          onChange={handleChange}
        />
        {errors.password && <p className="error-text">{errors.password}</p>}

        {errors.general && <p className="error-text">{errors.general}</p>}

        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
