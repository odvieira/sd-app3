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
    const [resource1, setResource1] = useState('DISCONNECTED')
    const [resource2, setResource2] = useState('DISCONNECTED')
    const [user, setUser] = useState(uname)
    const [resource, setResource] = useState('1')
    const navigate = useNavigate()
    const hostAddress = "http://localhost:5000"

    var statusListener1 = new EventSource("http://localhost:5000/stream?channel=" + user + '1');
    var statusListener2 = new EventSource("http://localhost:5000/stream?channel=" + user + '2');

    statusListener1.addEventListener(
        'message',
        e => { setResource1(e.data) },
        false
    );

    statusListener2.addEventListener(
        'message',
        e => { setResource2(e.data) },
        false
    );
    
    const handleAcquire = () => {
        resource == '1' ? setResource1('WANTED') : setResource2('WANTED')
        
        axios({
            method: 'get',
            url: hostAddress + "/acquire/" + user + "/" + resource,
            responseType: 'text'
        })
            .then(function (response) {
                console.log(response.data)
            });

    }

    const handleRelease = () => {
        axios({
            method: 'get',
            url: hostAddress + "/release/" + user + "/" + resource,
            responseType: 'text'
        })
            .then(function (response) {
                console.log(response.data)
            });
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
            </div>
        )
    }

    return (
        <div>
            <Bar />
            <div className="ServiceBody" style={{ padding: 30 }}>
                <h1>Hello, {user}!</h1>
                <Stack gap={4} className="col-md-5 mx-auto" style={{margin: 40}}>
                    <Button
                        variant="success"
                        onClick={() => handleAcquire()}>
                        Acquire Lock
                    </Button>
                    <Button
                        variant="success"
                        onClick={() => handleRelease()}>
                        Release Lock
                    </Button>
                    <Button
                        variant="secondary"
                        onClick={() => resource === '1' ? setResource('2') : setResource('1')}>
                        Toggle Resource: {resource}
                    </Button>
                </Stack>
                <br />
                <p className="status-label">Resource 1 status: {resource1}</p>
                <p className="status-label">Resource 2 status: {resource2}</p>
            </div>
        </div>
    )
}
