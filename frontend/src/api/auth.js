const FLASK_API_BASE = "http://localhost:5000/auth";

export async function POST(req) {
    try {
        const { pin, username, password } = await req.json();

        let endpoint = "";
        let payload = {};

        if (pin) {
            endpoint = `${FLASK_API_BASE}/pin`;
            payload = { pin };
        } else if (username && password) {
            endpoint = `${FLASK_API_BASE}/login`;
            payload = { username, password };
        } else {
            return Response.json({ error: "Invalid request data" }, { status: 400 });
        }

        // Send request to Flask backend
        const flaskResponse = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await flaskResponse.json();
        const status = flaskResponse.status;

        if (!flaskResponse.ok) {
            return Response.json({ error: data.error || "Authentication failed" }, { status });
        }

        return Response.json(data, { status });

    } catch (error) {
        console.error("❌ Authentication API Error:", error);
        return Response.json({ error: "Internal Server Error" }, { status: 500 });
    }
}
