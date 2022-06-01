import { useState } from "react"
import Form from 'react-bootstrap/Form'
import { useNavigate } from "react-router-dom"
import Button from 'react-bootstrap/Button'
import { useStore } from 'zustand'

export default function Home (){
    const [inputName, setInputName] = useState('')
    const setUsername = useStore(state => state.setUsername)
    const history = useNavigate()

    const handler = () => {
        setUsername(inputName)

        history.push("/courses")
    }

    return (
        <div>
            <Form>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="client"
                        onChange={e => setInputName(e.target.value)}
                    />
                    <Button variant="dark" onClick={handler}>
                        Create Client
                    </Button>
                </Form.Group>
            </Form>
        </div>
    )
}
  