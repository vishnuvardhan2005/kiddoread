import React from "react";
import { Link } from 'react-router-dom'
import Button from 'react-bootstrap/Button';

function Home() {
    return (
        <div className="home container">
            <Link to='/register'>
                <Button variant="link">Register</Button>
            </Link>
            <br />
            <Link to='/login'>
                <Button variant="link">Login</Button>
            </Link>
        </div>
    )
}
export default Home;