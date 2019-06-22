import React, { Component } from 'react';
import './Dashboard.css';

import ResultPanel from './ResultPanel';
import QueryPanel from './QueryPanel';

type DashboardProps = {}
type DashboardState = {
  query: string
}

export default class Dashboard extends Component<DashboardProps, DashboardState> {

  constructor(props: DashboardProps) {
    super(props);
  }

  render() {
    return (
      <div className="dashboard">
        <div className="home-component query-panel">
          <QueryPanel />
        </div>
        <div className="home-component result-panel">
          <ResultPanel seriesName="Black Mirror" />
        </div>
      </div>
    )
  }
}