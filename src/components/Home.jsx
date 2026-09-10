import { Link } from "react-router-dom";
import Navbar from "./Navbar";
import "./Home.css";
function Home() {
    return(
    
        <div  className="Ekhaya">
            <Navbar/>
             <h1>
                <span>Youth-Link</span>
            </h1>
            <p>UNLOCK YOUR FULL POTENTIAL</p>
            <p> Connecting the youth to a greater future</p>
            <Link to = "/SignUp">
            <button className="SignUp-btn">Get Started</button>
            </Link>
        </div>
        
    );
}

export default Home;