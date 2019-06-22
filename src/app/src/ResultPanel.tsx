import React, { Component } from 'react';
import Axios from 'axios';
import './ResultPanel.css';

type ResultPanelProps = {
  seriesName: string | undefined
}

type ResultPanelState = {
  tvSeries: any,
  responseStatus: Number | undefined
}

type EpisodeRatingObj = {
  rating: number,
  [key: string]: any
}

type SeasonRatingsObj = {
  ratings: Array<EpisodeRatingObj>,
  [key: string]: any
}

export default class ResultPanel extends Component<ResultPanelProps, ResultPanelState> {

  constructor(props: ResultPanelProps) {
    super(props);
    this.state = {
      tvSeries: undefined,
      responseStatus: undefined
    }
  }

  fetchTvStatistics = async (seriesName: string) => {
    const BASE_URL = 'http://localhost:8001';
    try {
      const response = await Axios.get(`${BASE_URL}/tv-series`, {
        params: { name: seriesName }
      })
      console.log(response);
      this.setState({
        tvSeries: response.data,
        responseStatus: response.status,
      });
    } catch (err) {
      console.log(err.response);
      this.setState({
        responseStatus: err.response.status
      })
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

  renderSeasonRatings(allRatings: Array<SeasonRatingsObj>) {
    return allRatings.map((seasonRatingsObj: SeasonRatingsObj) => {
      const seasonNum = seasonRatingsObj['_id'];
      return (
        <div className="tv-series-season" key={seasonNum}>
          <h2>Season {seasonNum}</h2>
          {this.renderEpisodeRating(seasonRatingsObj.ratings)}
        </div>
      );
    })
  }

  renderDetailedRatings = () => {
    const ratings = this.state.tvSeries['ratings'];
    return (
      <div className="tv-series">
        <h1>{this.state.tvSeries['name']}</h1>
        <div className="ratings-grid">
          {this.renderSeasonRatings(ratings)}
        </div>
      </div>
    )
  }

  renderPlaceholder = () => {
    return (
      <h1>Please enter a TV Series name  +_+ </h1>
    )
  }

  renderLoadingMessage = () => {
    return (<h1>Loading...</h1>)
  }

  renderRatingsDecodeError = () => {
    return (<p className="helper-msg">An error has occured in decoding the ratings object.</p>)
  }

  renderRatingsNotFound = () => {
    if (this.props.seriesName === undefined) {
      return this.renderRatingsDecodeError();
    }

    const seriesNameCapitalized = (() => {
      return this.props.seriesName === undefined ? "" : this.props.seriesName.split(" ").map((word) => {
        return word[0].toUpperCase() + word.slice(1);
      }).join(" ");
    })();

    return (
      <div>
        <h1>Sorry, we're unable to find '{seriesNameCapitalized}'</h1>
        <p className="helper-msg">
          This is most likely because our background worker has not processed this series yet =( 
          Please try again sometime soon =)
        </p>
      </div>
    )
  }

  renderRatings = () => {
    if (this.state.responseStatus === 404 && this.props.seriesName !== undefined) {
      return this.renderRatingsNotFound();
    }
    else if (this.state.responseStatus === 200) {
      return this.renderDetailedRatings();
    }
    else if (this.state.responseStatus === undefined) {
      return this.renderLoadingMessage();
    }
    else {
      return this.renderRatingsDecodeError();
    }
  }

  render() {
    const displayContent = this.props.seriesName === undefined ?
      this.renderPlaceholder() : this.renderRatings();
    return (
      <div className="">
        {displayContent}
      </div>
    )
  }
}