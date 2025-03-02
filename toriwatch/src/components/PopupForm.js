'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

function PopupForm() {
    const router = useRouter();
    const [error, setError] = useState(null);
    const [pin, setPin] = useState("");
    const [response, setResponse] = useState(null);

    // Handle input changes
    const handleChange = (e) => {
        setPin(e.target.value);
    };

    // Validate input
    const validateInput = (e) => {
        const { value } = e.target;
        console.log(`Validating PIN: ${value}`);

        // Example validation (Replace with actual DB check if needed)
        if (value.length !== 6 || isNaN(value)) {
            setError("❌ PIN must be exactly 6 numbers.");
        } else {
            setError(null);
        }
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!pin) {
            console.warn("⚠️ No PIN entered.");
            setError("PIN is required.");
            return;
        }

        console.log("📩 Sending PIN to background.js:", pin);
        chrome.runtime.sendMessage({ action: "sendPin", pin }, (response) => {
            console.log("✅ Response from background.js:", response);
            setResponse(response);
        });

        // Simulate authentication success
        router.push("/");
    };

    return (
        <div className='w-auto rounded-md'>
            <div>
                {error && <p className="text-red-500 text-center">{error}</p>}
                <form className="mt-4 space-y-4" onSubmit={handleSubmit}>
                    <label className="floating-label validator">
                        <span>Pin</span>
                        <input
                            type="number"
                            name="Pin"
                            placeholder="Enter 6-digit PIN"
                            className="input input-bordered w-full"
                            minLength="6"
                            maxLength="6"
                            pattern="\d{6}"
                            title="Must be exactly 6 numbers"
                            required
                            value={pin}
                            onChange={handleChange}
                            onBlur={validateInput} // Validate when input loses focus
                        />
                    </label>
                    <p className="validator-hint hidden">
                        Must be exactly 6 numbers
                    </p>
                    <button type="submit" className="btn btn-primary w-full">
                        Authenticate
                    </button>
                </form>
            </div>
        </div>
    );
}

export default PopupForm;
