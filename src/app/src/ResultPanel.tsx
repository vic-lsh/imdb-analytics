import React, { Component } from 'react';
import Axios from 'axios';
import styled from 'styled-components';
import { Line } from 'react-chartjs-2';
import { StyledH1 } from './Dashboard';
import { PlotColors } from './styles';

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

const NETWORK_ERR_INTERNAL = 0;

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
      if (err.response === undefined) {
        this.setState({
          responseStatus: NETWORK_ERR_INTERNAL
        })
      } else {
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
    else if (this.state.responseStatus === NETWORK_ERR_INTERNAL) {
      return <RatingsFetchingNetworkError />
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

const pickRandomColor = (colorObj: { [key: string]: string }) => {
  const keys = Object.keys(colorObj);
  return colorObj[keys[keys.length * Math.random() << 0]];
}

const RatingsDetail: React.FC<{ tvSeries: any }> = (props) => {
  return (
    <div className="tv-series">
      <StyledH1>{props.tvSeries['name']}</StyledH1>
      <RatingsPlot tvSeries={props.tvSeries} plotColor={pickRandomColor(PlotColors)} />
      <StyledRatingsGridDiv>
        <SeasonRatingsList seasonRatings={props.tvSeries.ratings} />
      </StyledRatingsGridDiv>
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
    <StyledSeasonRatingDiv>
      <h2>Season {props.seasonRating['_id']}</h2>
      <EpisodeRatingsList ratingsInSeason={props.seasonRating.ratings} />
    </StyledSeasonRatingDiv>
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
    <StyledEpisodeRatingDiv>
      <StyledEpNumSpan>E{epNum}</StyledEpNumSpan>
      <StyledEpRatingSpan>{props.episodeRating['rating']}</StyledEpRatingSpan>
    </StyledEpisodeRatingDiv>
  );
}

const flattenArray = (arr: Array<any>) => {
  return [].concat.apply([], arr);
}

const extractRatingNumbers = (tvSeries: any) => {
  return tvSeries.ratings.map((seasonRating: SeasonRatingsObj) => {
    return seasonRating.ratings.map((epRating: EpisodeRatingObj) => {
      return epRating.rating;
    })
  });
}

const extractEpisodeLabels = (tvSeries: any) => {
  return tvSeries.ratings.map((seasonRating: SeasonRatingsObj) => {
    const seasonNum = seasonRating['_id'];
    return seasonRating.ratings.map((epRating: EpisodeRatingObj) => {
      return `S${seasonNum}E${epRating['_id']}`;
    })
  });
}

const RatingsPlot: React.FC<{ tvSeries: any, plotColor: string }> = (props) => {

  const ratings = flattenArray(extractRatingNumbers(props.tvSeries));
  const labels = flattenArray(extractEpisodeLabels(props.tvSeries));

  const plotOptions = {
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines: {
          drawOnChartArea: false
        },
      }],
      yAxes: [{
        gridLines: {
          drawOnChartArea: false
        },
        ticks: {
          max: 10,
          min: Math.min(...ratings, 5),
        }
      }]
    }
  }

  return (
    <StyledRatingsPlotDiv>
      <Line width={100} height={20}
        data={{
          labels: labels,
          datasets: [{
            data: ratings,
            label: props.tvSeries.name,
            borderColor: props.plotColor,
            fill: false
          }]
        }}
        options={plotOptions}
      />
    </StyledRatingsPlotDiv>)
}

const RatingsNotFound: React.FC<{ seriesName: string }> = (props) => {
  const seriesNameCapitalized = (() => {
    if (props.seriesName === undefined) {
      return "";
    }

    const seriesName = props.seriesName.trim();
    if (seriesName === "") {
      return seriesName;
    }

    return seriesName.split(" ").map((word) => {
      return word[0].toUpperCase() + word.slice(1);
    }).join(" ");
  })();

  return (
    <div>
      <StyledH1>Sorry, we're unable to find '{seriesNameCapitalized}'</StyledH1>
      <StyledHelperMsg>
        This is most likely because our background worker has not processed this series yet =(
        Please try again sometime soon =)
      </StyledHelperMsg>
    </div>
  )
}

const RatingsLoading: React.FC = () => {
  return (<StyledH1>Loading...</StyledH1>)
}

const RatingsFetchingNetworkError: React.FC = () => {
  return (
    <React.Fragment>
      <ErrorHeader />
      <StyledHelperMsg>
        An error has occured in fetching the ratings data.
      </StyledHelperMsg>
      <StyledHelperMsg>
        Admin: please double check if the server has been started.
      </StyledHelperMsg>
    </React.Fragment>
  )
}

const RatingsDecodeError: React.FC = () => {
  return (<StyledHelperMsg>An error has occured in decoding the ratings object.</StyledHelperMsg>)
}

const Placeholder: React.FC = () => {
  return (<StyledH1>Please enter a TV Series name  +_+ </StyledH1>)
}

const ErrorHeader: React.FC = () => {
  return (<StyledH1>An error has occured...oops :(</StyledH1>)
}

const StyledEpNumSpan = styled.span`
  font-weight: bold;
`;

const StyledEpRatingSpan = styled.span``;

const StyledEpisodeRatingDiv = styled.div`
  padding: 0 0.3rem 0;
  display: grid;
  grid-template-columns: 40% 60%;
`;

const StyledSeasonRatingDiv = styled.div`
  padding: 0 1rem 1rem 1rem;
`;

const StyledRatingsGridDiv = styled.div`
  display: grid; 
  grid-template-columns: repeat(auto-fit, minmax(150px, 2fr));
`;

const StyledRatingsPlotDiv = styled.div`
  padding: 2rem 0 0;
`;

const StyledHelperMsg = styled.p`
  padding: 0 1rem;
  font-size: 1.4rem;
`;