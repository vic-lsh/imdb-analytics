import './App.css';
import ResultPanel from './ResultPanel';
import QueryPanel from './QueryPanel';

const React = require('react');


const App: React.FC = () => {

  return (
    <div className="App">
      <div className="home-component query-panel">
        <QueryPanel />
      </div>
      <div className="home-component dashboard">
        <ResultPanel seriesName="Black Mirror" />
      </div>
    </div>
  );
}

export default App;
