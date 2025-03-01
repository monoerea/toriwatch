import PropTypes from "prop-types";
import Link from "next/link";

function NavBar({ items }) {
  return (
    <nav className="navbar shadow-sm">
    <div className="flex-1">
        <Link href="/" className="link link-hover hover:text-primary">toriwatch</Link>
    </div>
      <div role="tablist" className="tabs tab-border">
        <span className=""></span>
        {items.map((item) => (
          <li key={item.id} className="tab">
            <Link href={item.link} className="capitalize hover:text-primary">
              {item.label}
            </Link>
          </li>
        ))}
      </div>
    </nav>
  );
}

NavBar.propTypes = {
  items: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      label: PropTypes.string.isRequired,
      link: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default NavBar;
