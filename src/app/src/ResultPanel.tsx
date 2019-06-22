import React, { Component } from 'react';
import Axios from 'axios';
import './ResultPanel.css';

type ResultPanelProps = {
  seriesName: string | undefined
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

  fetchIfNotUndefined = () => {
    if (this.props.seriesName !== undefined) {
      this.fetchTvStatistics(this.props.seriesName);
    }
  }

  componentDidMount() {
    this.fetchIfNotUndefined();
  }

  componentDidUpdate(prevProps: ResultPanelProps) {
    if (this.props.seriesName !== prevProps.seriesName) {
      this.fetchIfNotUndefined();
    }
  }

  renderEpisodeRating(seasonRating: Array<EpisodeRatingObj>) {
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
          {this.renderEpisodeRating(seasonRatingsObj.ratings)}
        </div>
      );
    })
  }

  renderPlaceholder = () => {
    return (
      <p>Please enter a TV Series name.</p>
    )
  }

  renderRatings = () => {
    if (this.state.tvSeries === undefined) {
      return (<p>Loading...</p>)
    } else {
      const ratings = this.state.tvSeries['ratings'];
      return (
        <div className="tv-series">
          <h1>{this.state.tvSeries['_id']}</h1>
          <div className="ratings-grid">
            {this.renderSeasonRatings(ratings)}
          </div>
        </div>
      )
    }
  }

  render() {
    if (this.props.seriesName === undefined) {
      return this.renderPlaceholder();
    } else {
      return this.renderRatings();
    }
  }
}