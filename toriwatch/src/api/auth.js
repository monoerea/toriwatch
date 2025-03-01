export async function POST(req) {
    const { username, password } = await req.json();
  
    // Simulated auth (Replace with real database lookup)
    if (username === "admin" && password === "password123") {
      return Response.json({ success: true }, { status: 200 });
    } else {
      return Response.json({ error: "Invalid credentials" }, { status: 401 });
    }
  }
  