// pages/popup.js
export default function Popup() {
    return (
        <div className="p-4 w-[400px] h-[600px] bg-base-100">
        <h1 className="text-2xl font-bold text-primary">My Chrome Extension Popup</h1>
        <p className="mt-2 text-base-content">
            This is a styled popup built with Next.js, Tailwind CSS, and DaisyUI!
        </p>
        <button
            className="mt-4 btn btn-primary"
            onClick={() => alert("Button clicked!")}
        >
            Click Me
        </button>
        </div>
    );
}