import './App.scss'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Layout from "./pages/Layout.jsx"
import Home from "./pages/Home.jsx"
import NoPage from "./pages/NoPage.jsx"
import Service from './pages/Service.jsx'
import create from 'zustand'

const useStore = create((set) => ({
  username: '',
  isUsernameSet: false,
  setUsername: () => set((newValue) => ({
    username: newValue,
    isUsernameSet: true
  })),
  disconnect: () => set(() => ({
    username: '',
    isUsernameSet: false
  }))
}))


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path='/home' element={<Home />} />
          <Route path='/service' element={<Service />} />
          <Route path="*" element={<NoPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
