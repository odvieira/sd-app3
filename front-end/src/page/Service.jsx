import { useState } from "react"
import Button from "react-bootstrap/Button"
import { useNavigate } from "react-router-dom"
import useStore from "../data/Store"
import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'
import Stack from 'react-bootstrap/Stack'
import axios from 'axios'

export default function Service() {
    const uname = useStore(state => state.username)
    const [selfStatus, setSelfStatus] = useState('DISCONNECTED')
    const [user, setUser] = useState(uname)
    const [resource, setResource] = useState('1')
    const navigate = useNavigate()
    var source = new EventSource("http://localhost:5000/stream?channel=" + user);
    const hostAddress = "http://localhost:5000"

    source.addEventListener('message', function (event) {
        console.log([user, event.data])
    }, false);

    source.addEventListener('error', function (event) {
        console.log(event.data);
    }, false);

    handleAcquire = () => {
        axios({
            method: 'get',
            url: hostAddress + "/acquire/" + user + "/" + resource,
            responseType: 'text'
        })
            .then(function (response) {
                console.log(response.data)
            });

    }

    handleRelease = () => {

    }

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
                        <Button
                            variant="primary"
                            onClick={() => handleAcquire()}>
                            Acquire Lock
                        </Button>
                        <Button
                            variant="outline-primary"
                            onClick={() => handleRelease()}>
                            Release Lock
                        </Button>
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
