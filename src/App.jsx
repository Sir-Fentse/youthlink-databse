import Home from "./components/Home";
import{Routes, Route} from "react-router-dom";
import SignUp from "./components/SignUp";
import Login from "./components/Login";
import Opportunities from "./components/Opportunities";
import Contact from "./components/Contact";
import About from "./components/About";
import "./App.css";
function App() {

  return (
    
    <Routes>
      <Route path="/Home" element={<Home/>} />
      <Route path= "/SignUp" element = {<SignUp/>} />
      <Route path="/Login" element= {<Login/>} />
      <Route path="/" element= {<Opportunities/>} />
      <Route path="/Contact" element= {<Contact/>} />
      <Route path="/About" element= {<About/>} />

    </Routes>

 
  );
}

export default App;