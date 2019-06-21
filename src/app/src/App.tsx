import './App.css';
import Dashboard from './Dashboard';
import QueryPanel from './QueryPanel';

const React = require('react');


const App: React.FC = () => {

  return (
    <div className="App">
      <div className="home-component query-panel">
        <QueryPanel />
      </div>
      <div className="home-component dashboard">
        <Dashboard seriesName="Black Mirror" />
      </div>
    </div>
  );
}

export default App;
