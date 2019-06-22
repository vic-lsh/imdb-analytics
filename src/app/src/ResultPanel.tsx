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
      if (err.response !== undefined) {
        this.setState({
          responseStatus: err.response.status
        })
      }
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

  renderRatings = () => {
    if (this.state.responseStatus === 404 && this.props.seriesName !== undefined) {
      return <RatingsNotFound seriesName={this.props.seriesName} />
    }
    else if (this.state.responseStatus === 200) {
      return <RatingsDetail tvSeries={this.state.tvSeries} />
    }
    else if (this.state.responseStatus === undefined) {
      return <RatingsLoading />
    }
    else {
      return <RatingsDecodeError />
    }
  }

  render() {
    const displayedContent = this.props.seriesName === undefined ?
      <Placeholder /> : this.renderRatings();
    return (
      <div className="">
        {displayedContent}
      </div>
    )
  }
}

const RatingsDetail: React.FC<{ tvSeries: any }> = (props) => {
  return (
    <div className="tv-series">
      <h1>{props.tvSeries['name']}</h1>
      <div className="ratings-grid">
        <SeasonRatingsList seasonRatings={props.tvSeries.ratings} />
      </div>
    </div>
  )
}

const SeasonRatingsList: React.FC<{ seasonRatings: SeasonRatingsObj[] }> = (props) => {
  return (<React.Fragment>{
    props.seasonRatings.map((seasonRating) => {
      return <SeasonRating seasonRating={seasonRating} key={seasonRating['_id']} />
    })
  }</React.Fragment>)
}

const SeasonRating: React.FC<{ seasonRating: SeasonRatingsObj }> = (props) => {
  return (
    <div className="tv-series-season">
      <h2>Season {props.seasonRating['_id']}</h2>
      <EpisodeRatingsList ratingsInSeason={props.seasonRating.ratings} />
    </div>
  );
}

const EpisodeRatingsList: React.FC<{ ratingsInSeason: EpisodeRatingObj[] }> = (props) => {
  return (<React.Fragment>{
    props.ratingsInSeason.map((epRating) => {
      return <EpisodeRating episodeRating={epRating} key={epRating['_id']} />
    })
  }</React.Fragment>)
}

const EpisodeRating: React.FC<{ episodeRating: EpisodeRatingObj }> = (props) => {
  const epNum = props.episodeRating['_id'];
  return (
    <div className="episode-rating">
      <div className="ep-num">E{epNum}</div>
      <div className="ep-rating">{props.episodeRating['rating']}</div>
    </div>
  );
}

const RatingsNotFound: React.FC<{ seriesName: string }> = (props) => {
  const seriesNameCapitalized = (() => {
    return props.seriesName === undefined ? "" : props.seriesName.split(" ").map((word) => {
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

const RatingsLoading: React.FC = () => {
  return (<h1>Loading...</h1>)
}

const RatingsDecodeError: React.FC = () => {
  return (<p className="helper-msg">An error has occured in decoding the ratings object.</p>)
}

const Placeholder: React.FC = () => {
  return (<h1>Please enter a TV Series name  +_+ </h1>)
}