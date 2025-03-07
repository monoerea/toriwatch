    "use client";
    import PopupForm from "@/components/PopupForm";
    import ToggleButton from "@/components/ToggleButton";
    import { useEffect, useRef, useState } from "react";

    export default function Popup() {
        const authLink = "https://www.example.com";
        const [isChecked, setIsChecked] = useState(false);
        const handleToggle = (e) => {
            setIsChecked(!isChecked); // Toggle the state
        };
        const cardRef = useRef(null);

        useEffect(() => {
            const updateHeight = () => {
                if (cardRef.current) {
                    const newHeight = cardRef.current.scrollHeight;
                    console.log("📩 Sending card height:", newHeight);
                    window.parent.postMessage({ height: newHeight }, "*");
                }
            };

            updateHeight(); // Run on mount

            // Observe changes in the `.card` div and update height dynamically
            const observer = new MutationObserver(updateHeight);
            if (cardRef.current) {
                observer.observe(cardRef.current, { childList: true, subtree: true, attributes: true });
            }

            return () => observer.disconnect();
        }, []);

        return (
            <div ref={cardRef} className="card p-4 bg-base-100">
                <ToggleButton
                    legend={"ToriWatch"}
                    handleToggle={handleToggle}
                    isChecked={isChecked}
                >
                    {/* Content inside the ToggleButton */}
                    <h1 className="card-title text-2xl font-bold text-primary">
                        Authenticate your X account.
                    </h1>
                    <div className="mt-2 text-base-content">
                        <ol className="list-decimal list-inside space-y-2 text-sm">
                            <li className="mb-2">
                                Go to the generated link below{" "}
                                <a
                                    href={authLink}
                                    className="bg-black/[.05] dark:bg-white/[.06] px-1 py-0.5 rounded font-semibold"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    {authLink}
                                </a>
                            </li>
                            <li className="mb-2">Input the pin to the field below.</li>
                        </ol>
                    </div>
                    <PopupForm /> {/* Extra content (PopupForm) */}
                </ToggleButton>
            </div>
        );
    }