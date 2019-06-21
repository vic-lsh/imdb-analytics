import React, { Component } from 'react';
import Axios from 'axios';

type DashboardState = {
  tvSeries: any
}

type EpisodeRatingObj = {
  rating: number,
  [key: string]: any
}

type TVSeriesRatingsObj = {
  ratings: Array<EpisodeRatingObj>,
  [key: string]: any
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

  renderEpisodeRatings(seasonRating: Array<EpisodeRatingObj>) {
    return seasonRating.map((episodeRating: EpisodeRatingObj) => {
      const epNum = episodeRating['_id'];
      return <li key={epNum}>{epNum}: {episodeRating['rating']}</li>;
    })
  }

  renderRatings() {
    const ratings = this.state.tvSeries['ratings'];
    return ratings.map((seasonRatingsObj: TVSeriesRatingsObj) => {
      return (
        <div>
          <h2>Season {seasonRatingsObj['_id']}</h2>
          <ul>{this.renderEpisodeRatings(seasonRatingsObj.ratings)}</ul>
        </div>
      );
    })
  }

  render() {
    if (this.state.tvSeries === undefined) {
      return (<p>loading...</p>);
    }
    else {
      const ratingsList = this.renderRatings();
      return (
        <div>
          <h1>{this.state.tvSeries['_id']}</h1>
          <div>{ratingsList}</div>
        </div>
      )
    }
  }
}