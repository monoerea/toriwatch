import LoginForm from "@/components/LoginForm";

export default function LoginPage() {
  return (
      <div className="flex flex-col items-center justify-center sm:items-center">
        <h1 className="text-3xl font-bold">Login Page</h1>
          <LoginForm />
      </div>
  );
}