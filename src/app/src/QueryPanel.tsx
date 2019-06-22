import React, { Component } from 'react';
import './QueryPanel.css';

type QueryPanelProps = {
  setQueryInParent: (value: string) => void;
}

type QueryPanelState = {
  query: string
}

export default class QueryPanel extends Component<QueryPanelProps, QueryPanelState> {

  constructor(props: QueryPanelProps) {
    super(props);
    this.state = {
      query: ""
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event: any) {
    this.setState({ query: event.target.value });
  }

  handleSubmit(event: any) {
    this.props.setQueryInParent(this.state.query);
    this.setState({ query: "" });
    event.preventDefault();
  }

  handleEnterKey(event: any) {
    if (event.keyCode === 13) {
      this.handleSubmit(event);
    }
  }

  render() {
    return (
      <form className="search-form">
        <label className="input-label">
          <h1>TV Series</h1>
          <input className="search-field" type="text" name="tv-series"
            value={this.state.query} onChange={this.handleChange} 
            onKeyDown={this.handleEnterKey} />
        </label>
        <button className="submit-btn" type="submit" onClick={this.handleSubmit}>
          Search
        </button>
      </form>
    )
  }
}