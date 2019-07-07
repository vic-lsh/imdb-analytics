import styled from 'styled-components';
import Dashboard from './Dashboard';

const React = require('react');


const App: React.FC = () => {

  return (
    <StyledAppDiv>
      <Dashboard />
    </StyledAppDiv>
  );
}

const StyledAppDiv = styled.div`
  overflow: hidden;
  height: 100%;
  width: 100%;
`;

export default App;
