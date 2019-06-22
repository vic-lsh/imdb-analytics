import React, { Component } from 'react';
import Axios from 'axios';
import './ResultPanel.css';

type ResultPanelProps = {
  seriesName: string
}

type ResultPanelState = {
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

export default class ResultPanel extends Component<ResultPanelProps, ResultPanelState> {

  constructor(props: ResultPanelProps) {
    super(props);
    this.state = {
      tvSeries: undefined
    }
  }

  async fetchTvStatistics(seriesName: string) {
    const BASE_URL = 'http://localhost:8001';
    try {
      const response = await Axios.get(`${BASE_URL}/tv-series`, {
        params: { name: seriesName }
      })
      this.setState({ tvSeries: response.data });
    } catch (err) {
      console.log(err);
    }
  }

  componentDidMount() {
    this.fetchTvStatistics(this.props.seriesName);
  }

  renderEpisodeRatings(seasonRating: Array<EpisodeRatingObj>) {
    return seasonRating.map((episodeRating: EpisodeRatingObj) => {
      const epNum = episodeRating['_id'];
      return (
        <div className="episode-rating" key={epNum}>
          <div className="ep-num">E{epNum}</div>
          <div className="ep-rating">{episodeRating['rating']}</div>
        </div>
      );
    })
  }

  renderSeasonRatings(allRatings: Array<TVSeriesRatingsObj>) {
    return allRatings.map((seasonRatingsObj: TVSeriesRatingsObj) => {
      const seasonNum = seasonRatingsObj['_id'];
      return (
        <div className="tv-series-season" key={seasonNum}>
          <h2>Season {seasonNum}</h2>
          {this.renderEpisodeRatings(seasonRatingsObj.ratings)}
        </div>
      );
    })
  }

  renderRatings() {
    const ratings = this.state.tvSeries['ratings'];
    return (
      <div className="ratings-grid">
        {this.renderSeasonRatings(ratings)}
      </div>
    )
  }

  render() {
    if (this.state.tvSeries === undefined) {
      return (<p>loading...</p>);
    }
    else {
      const ratingsList = this.renderRatings();
      return (
        <div className="tv-series">
          <h1>{this.state.tvSeries['_id']}</h1>
          <div>{ratingsList}</div>
        </div>
      )
    }
  }
}