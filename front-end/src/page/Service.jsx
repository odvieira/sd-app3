import { useState } from "react"
import Button from "react-bootstrap/Button"
import { useNavigate } from "react-router-dom"
import useStore from "../data/Store"
import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'
import Redis from "ioredis"

export default function Service() {
    const uname = useStore(state => state.username)
    const [selfStatus, setSelfStatus] = useState('RELEASED')
    const [user, setUser] = useState(uname)
    const navigate = useNavigate()
    const subscriber = Redis()

    subscriber.subscribe(user, (err, count) => err ? console.log([err]) : count)

    // Protocol: [KIND:str], [CHANNEL:str]. [MESSAGE:str]
    // The only kind I'm interested in is 'message'
    subscriber.on('message', (channel, message) => {
        setSelfStatus(message)
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
                    <Stack gap={2} className="col-md-5 mx-auto">
                        <Button variant="secondary">Acquire Lock</Button>
                        <Button variant="outline-secondary">Release Lock</Button>
                    </Stack>
                    <p className="status-label">Status: {selfStatus}</p>
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
