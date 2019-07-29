import React, { Component } from 'react';
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
      <StyledDashboardDiv className="dashboard">
        <StyledQueryPanelComponentDiv className="home-component query-panel">
          <QueryPanel setQueryInParent={this.handleQuerySubmission} />
        </StyledQueryPanelComponentDiv>
        <StyledResultPanelComponentDiv className="home-component result-panel">
          <ResultPanel seriesName={this.state.query} />
        </StyledResultPanelComponentDiv>
      </StyledDashboardDiv>
    )
  }
}

const StyledDashboardDiv = styled.div`
  text-align: left;
  height: 100vh;
`;

const StyledHomeComponentDiv = styled.div`
  padding-top: 5rem;
`;

const StyledQueryPanelComponentDiv = styled(StyledHomeComponentDiv)`
  background: #d1d1d1;
  width: 30vw;
  height: 100vh;
  position: fixed;
`;

const StyledResultPanelComponentDiv = styled(StyledHomeComponentDiv)`
  width: 70vw;
  height: 100vh;
  float: right;
`;

export const StyledH1 = styled.h1`
  margin: 0;
  font-size: 2.3rem;
`;

export const StyledH1DarkBg = styled(StyledH1)`
  color: white;
`;