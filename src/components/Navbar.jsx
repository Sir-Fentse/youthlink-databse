import { Link } from "react-router-dom";
function Navbar() {
    return (
        <nav>
            <h2>Youth-Link</h2>

            <ul>
                 <li><Link to = "/home">Home</Link></li>
                <li><a href="#Profile">Profile</a></li>
                <li><Link to = "/About">About</Link></li>
                <li><a href="#Contact">Contact</a></li>
                <li><Link to = "/login">Login</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;
