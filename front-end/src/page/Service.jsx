import { useState } from "react"
import Button from "react-bootstrap/Button"
import { useNavigate } from "react-router-dom"
import useStore from "../data/Store"
import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'
import { createClient } from 'redis';

export default function Service() {
    const uname = useStore(state => state.username)
    const [user, setUser] = useState(uname)
    const navigate = useNavigate()
    const subscriber = createClient();

    subscriber.on('error', (err) => console.log('Redis Client Error', err));

    await subscriber.connect();

    await subscriber.subscribe(user, (message) => {
        console.log(message); // 'message'
    });

    const Bar = () => {
        return (
            <div>
                <Navbar bg="dark" expand="lg">
                    <Container fluid>
                        <Button
                            variant="outline-success"
                            onClick={() => navigate("/")}>
                            Leave
                        </Button>
                    </Container>
                </Navbar>
                <div className="ServiceBody" style={{ padding: 30 }}>
                    <h1>Hello, {user}!</h1>
                </div>
            </div>
        )
    }

    return (
        <div>
            <Bar />
        </div>
    )
}
