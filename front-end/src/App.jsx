import './App.scss'
import Home from "./page/Home"
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"
import NoPage from "./page/NoPage"
import Service from './page/Service'

export default function App() {
  return (
    <div className='App'>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path='/home' element={<Home />} />
          <Route path='/service' element={<Service />} />
          <Route path="*" element={<NoPage />} />
        </Routes>
      </Router>
    </div>
  )
}
