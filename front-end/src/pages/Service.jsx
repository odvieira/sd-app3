import { useStore } from 'zustand'

export default function Service(){
    const username = useStore(state => state.username)
    
    return (
        <div>
            <h1>Hello, {username}!</h1>
        </div>
    )
}
  