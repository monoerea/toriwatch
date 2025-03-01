'use client';
import { useState } from "react";
import { useRouter } from "next/navigation";
import { handleLogin, handleTwitterAuth } from "@/controllers/authControllers";
import Image from "next/image";

export default function LoginForm() {
  const router = useRouter();
  const [formData, setFormData] = useState({ Email: "", password: "" });
  const [error, setError] = useState(null);

  const handleChange = async (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validateInput = async (e) => {
    e.preventDefault();
    console.log("Logging e",e); 
    const { name, value } = e.target;
    console.log(`Validating ${name}: ${value}`)
    //TODO: Must not contain any dupes based on the db
    };
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await handleLogin(formData);
      router.push("/dashboard");
    } catch (err) {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="w-full max-w-md px-6 py-5 bg-base-300 shadow-md rounded-lg">
      <h2 className="text-2xl font-semibold text-center">Authenticate Toriwatch</h2>

      {error && <p className="text-red-500 text-center">{error}</p>}

      <form className="mt-4 space-y-4" onSubmit={handleSubmit}>
      <label className="floating-label validator">
          <span>Email</span>
          <input
            type="email"
            name="Email"
            placeholder="Username"
            className="input input-bordered w-full"
            title="Email"
            required
            onChange={handleChange}
            onInput={validateInput}
          />
        </label>
        <p className="validator-hint hidden">
          Username taken.
        </p>
        <label className="floating-label validator">
          <span>Password</span>
          <input
            type="password"
            name="password"
            placeholder="Password"
            className="input input-bordered w-full"
            minLength="8"
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
            title="Must be more than 8 characters, including number, lowercase letter, uppercase letter"
            required
            onInput={validateInput}
          />
        </label>
        <p className="validator-hint hidden">
          Must be more than 8 characters, including:
          <br />At least one number
          <br />At least one lowercase letter
          <br />At least one uppercase letter
        </p>
        <button type="submit" className="btn btn-primary w-full">
          Login
        </button>
      </form>

      {/* OAuth Login */}
      <div className="divider">OR</div>
      <button className="btn btn-info hover:btn-accent w-full flex items-center gap-2" onClick={handleTwitterAuth}>
        <Image src="/twitter.svg" alt="Twitter Logo" width={20} height={20} />
        Login with X (Twitter)
      </button>

      <p className="mt-4 text-sm text-center">
        Don&apos;   t have an account? <a href="/auth/signup" className="text-blue-600 hover:underline">Sign up</a>
      </p>
    </div>
  );
}
