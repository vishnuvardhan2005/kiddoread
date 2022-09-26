import React, { useState } from 'react'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import { useNavigate } from "react-router-dom";

const Login = (props) => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate();

    const submitHandler = event => {
        console.log("submitting login")
        event.preventDefault();
        axios.post('login', {
            email: email,
            password: password
          })
          .then(function (response) {
            console.log("login response")
            console.log(response.data.access_token)
            props.setToken(response.data.access_token)
            navigate('/question')
          })
          .catch(function (error) {
            console.log(error);
          });
    }

    return (
        <div className='container'>
            <div className='form'>
                <form onSubmit={submitHandler}>
                    <Form.Group>
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" placeholder='your email' name="email" value={email}
                            onChange={(e) => { setEmail(e.target.value) }}
                        />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" name="password" value={password}
                            onChange={(e) => { setPassword(e.target.value) }}
                        />
                    </Form.Group>
                    <br />

                    <Form.Group>
                        <Button variant="primary" type="submit">
                            Login
                        </Button>
                    </Form.Group>

                </form>
            </div>
        </div>

    )
}

export default Login