import { useState, useEffect } from 'react'
import axios from "axios";
import React from 'react';
import { Navigate } from 'react-router-dom'
import FormText from 'react-bootstrap/esm/FormText';
import FormLabel from 'react-bootstrap/esm/FormLabel';
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/esm/Button';
import Card from 'react-bootstrap/Card'
import { useNavigate } from "react-router-dom";

function Question(props) {
  const [question, setQuestion] = useState([])
  const [answer, setAnswer] = useState('')
  const navigate = useNavigate();

  useEffect(() => {
    console.log("Getting a question")
    console.log(props.token)

    axios.get('question', {
      headers: {
        Authorization: 'Bearer ' + props.token,
      }
    })
      .then(function (response) {
        // handle success
        setQuestion(response.data)
        console.log(response.data);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });

  }, [])

  const handleSubmit = event => {
    console.log("Submitting answer " + answer)
    event.preventDefault();
    axios.post('question', {
      "question": question.question,
      "answer": answer
    }, {
      headers: {
        Authorization: 'Bearer ' + props.token,
      }
    }).then(function (response) {
      console.log("posted")
      // navigate('/question')
      window.location.reload();
    }).catch(function (error) {
      console.log(error)
    })
  }

  return props.token ? (
    question.gameOver == undefined ? (
      <div>
        <Card style={{ width: '18rem' }}>
          <Card.Body>
            <h4>Score: {question.score}</h4>
            <p>Question : {question.question}</p>
            <form onSubmit={handleSubmit}>
              <Form.Group>
                <Form.Label>Answer</Form.Label>
                <Form.Control type="text" onChange={(e) => setAnswer(e.target.value)} />
              </Form.Group>
              <br />

              <Form.Group>
                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form.Group>
            </form>
          </Card.Body>
        </Card>
      </div>
    ) : (
      <div>
        <h1>Game over. Score: {question.score}</h1>
      </div>
    )
  ) :
    (
      <Navigate to={{ pathname: '/login' }} />
    )
}

export default Question;