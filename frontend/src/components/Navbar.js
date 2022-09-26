import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import React from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';

function MyNavbar() {
  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="home">Kiddoread</Navbar.Brand>
        </Container>
      </Navbar>
    </>
  );
}

export default MyNavbar;