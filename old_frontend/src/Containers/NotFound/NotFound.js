import "./NotFound.css";
import { Link } from "react-router-dom";

export default function NotFound() {
    return (
        <div className="notFoundPage">
            <h1>Oops! You seem to be lost.</h1>
            <h4>Here are some helpful links:</h4>
            <div className="notFoundLinks">
                <Link to='/'>Home</Link>
            </div>
        </div>
    )
}