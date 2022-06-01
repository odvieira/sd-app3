import { useState } from "react"
import Form from 'react-bootstrap/Form'
import { useNavigate } from "react-router-dom"
import Button from 'react-bootstrap/Button'
import useStore from "../data/Store"
import Container from 'react-bootstrap/Container'
import './Home.scss'

export default function Home() {
    const [inputName, setInputName] = useState('')
    const setUsername = useStore(state => state.setUsername)
    const navigate = useNavigate()

    const handler = () => {
        setUsername(inputName)

        navigate("/service")
    }

    return (
        <div className="Home">       
            <Container className="HomeForm">
                <Form.Control
                    type="text"
                    placeholder="ID"
                    onChange={e => setInputName(e.target.value)}
                />
                <br />
                <Button onClick={handler}>
                    Create Client
                </Button>
            </Container>
        </div>
    )
}
