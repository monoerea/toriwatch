export const handleLogin = async (email, password) => {
  if (email === "test@example.com" && password === "P4ssword") {
    return { success: true, user: { email, name: "Test User" } };
  }
  return { success: false, error: "Invalid credentials" };
};

export const handleTwitterAuth = async(link,pin)=>{

}
