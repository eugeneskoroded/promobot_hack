import "./App.scss";
import { Header } from "./Components/Header";
import { Chat } from "./Components/Chat";

const App = () => {
  return (
    <div className="main-container">
      <div className="promobot-container">
        <Header />
        <Chat />
      </div>
    </div>
  );
};

export default App;
