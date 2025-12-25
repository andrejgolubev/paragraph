import Header from "./components/Header"
import MainContent from "./components/MainContent"
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
