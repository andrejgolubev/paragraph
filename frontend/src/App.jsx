import Header from "./components/Header"
import MainContent from "./components/MainContent"
import ScheduleContainer from "./components/ScheduleContainer"
import { Provider } from "./context/Provider"

function App() {
  return (
    <Provider>
      <Header />
      <MainContent />
    </Provider>
  )
}

export default App
