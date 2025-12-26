import Header from "./components/Header"
import ScheduleContent from "./components/ScheduleContent"
import { Provider } from "./context/Provider"
import {Route, Routes} from 'react-router-dom'


function App() {
  return (
    <Provider>
      <Header />

      <Routes>
        <Route path="/" element={<ScheduleContent />} />
      </Routes>
      
    </Provider>
  )
}

export default App
