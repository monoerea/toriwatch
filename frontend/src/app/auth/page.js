import LoginForm from "@/components/LoginForm";

export default function LoginPage() {
  return (
      <div className="flex flex-col items-center justify-center sm:items-center">
        <h1 className="text-2xl font-bold pb-10">Connect the app to your X account</h1>
          <LoginForm />
      </div>
  );
}