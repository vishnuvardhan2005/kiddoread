import React, { useState } from 'react'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import { useNavigate } from "react-router-dom";

const Register = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    // const [confirm_password, setConfirm_password] = useState('')
    const navigate = useNavigate();


    const submitForm = event => {
        console.log("submitting register")
        event.preventDefault();
        axios.post('register', {
            email:email,
            password:password
        }).then(function(response){
            console.log(response.data)
            navigate('/login')
        }).catch(function(error){
            console.log(error)
        })
    }

    return (
        <div className='container'>
            <div className='form'>
                <form onSubmit={submitForm}>
                    <Form.Group>
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" placeholder='your email' name="email" value={email}
                            onChange={(e) => { setEmail(e.target.value) }}
                        />
                    </Form.Group>
                    <br />
                    <Form.Group>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" name="password" value={password}
                            onChange={(e) => { setPassword(e.target.value) }}
                        />
                    </Form.Group>
                    {/* <Form.Group>
                        <Form.Label>Confirm password</Form.Label>
                        <Form.Control type="password" name="confirm_password" value={confirm_password}
                            onChange={(e) => { setConfirm_password(e.target.value) }} />
                    </Form.Group> */}
                    <br />

                    <Form.Group>
                        <Button variant="primary" type="submit">
                            Register
                        </Button>
                    </Form.Group>

                </form>
            </div>
        </div>

    )
}

export default Register