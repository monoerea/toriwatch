"use client";
import PropTypes from 'prop-types';
function ToggleButton({ legend , children, handleToggle, isChecked}) {

    return (
    <div className="flex flex-row">
        <fieldset className="fieldset p-4 bg-base-100 border border-base-300 rounded-box w-64 ">
            <legend className="fieldset-legend text-2xl">{legend}
            <input
            type="checkbox"
            className="toggle toggle-primary"
            checked={isChecked}
            onChange={handleToggle} />
            </legend>
            {isChecked ? children : <span className="text-center">Extension Off</span>}
        </fieldset>
    </div>
    )
}
ToggleButton.propTypes = {
    legend : PropTypes.string.isRequired,
    children: PropTypes.elementType.isRequired,
    handleToggle : PropTypes.func.isRequired,
    isChecked : PropTypes.bool.isRequired
};

export default ToggleButton