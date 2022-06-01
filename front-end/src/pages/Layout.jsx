import { Outlet } from "react-router-dom"
import Nav from 'react-bootstrap/Nav'
import Navbar from 'react-bootstrap/Navbar'
import Container from 'react-bootstrap/Container'

export default function Layout(){
  return (
    <div>
      <Navbar bg="dark" expand="lg" variant="dark">
      <Container>
          <Nav as="ul">
            <Nav.Item as="li">
              <Nav.Link href="/home">Home</Nav.Link>
            </Nav.Item>
          </Nav>
        </Container>
      </Navbar>
      <Outlet />
    </div>
  )
}
