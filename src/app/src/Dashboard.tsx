import React, { Component } from 'react';
import './Dashboard.css';

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