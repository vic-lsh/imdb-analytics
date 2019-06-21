import React, { Component } from 'react';
import Axios from 'axios';

type DashboardState = {
  tvSeries: any
}

export default class Dashboard extends Component<{}, DashboardState> {

  constructor(props: {}) {
    super(props);
    this.state = {
      tvSeries: undefined
    }
  }

  async fetchTvStatistics(seriesName: string) {
    try {
      const response = await Axios.get('http://localhost:8001/tv-series', {
        params: { name: seriesName }
      })
      this.setState({ tvSeries: response.data });
    } catch (err) {
      console.log(err);
    }
  }

  componentDidMount() {
    this.fetchTvStatistics('How to Sell Drugs Online (Fast)');
  }

  render() {
    return (
      <p>{JSON.stringify(this.state.tvSeries)}</p>
    )
  }
}