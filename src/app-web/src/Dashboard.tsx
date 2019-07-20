import React, { Component } from 'react';
import './Dashboard.css';
import styled from 'styled-components';

import ResultPanel from './ResultPanel';
import QueryPanel from './QueryPanel';

type DashboardProps = {}

type DashboardState = {
  query: string | undefined
}

export default class Dashboard extends Component<DashboardProps, DashboardState> {

  constructor(props: DashboardProps) {
    super(props);
    this.state = {
      query: undefined
    }
  }

  /**
   * Query submission handler.
   * 
   * Called when there is a submission event (ENTER, submission btn clicked, 
   * etc.) in the `QueryPanel`. `QueryPanel` calls this function to trigger 
   * an update to teh `query` state in this component, thus propagating a 
   * change to the `seriesName` in the `ResultPanel`.
   */
  handleQuerySubmission = (querySetInPanel: string) => {
    this.setState({ query: querySetInPanel })
  }

  render() {
    return (
      <div className="dashboard">
        <div className="home-component query-panel">
          <QueryPanel setQueryInParent={this.handleQuerySubmission} />
        </div>
        <div className="home-component result-panel">
          <ResultPanel seriesName={this.state.query} />
        </div>
      </div>
    )
  }
}

export const StyledH1 = styled.h1`
  margin: 0;
  font-size: 2.3rem;
`

export const StyledH1DarkBg = styled(StyledH1)`
  color: white;
`;