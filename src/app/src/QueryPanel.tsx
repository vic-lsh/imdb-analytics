import React, { Component } from 'react';
import './QueryPanel.css';

export default class QueryPanel extends Component<{}, {}> {

  render() {
    return (
      <form className="search-form">
        <label className="input-label">
          <h1>TV Series</h1>
          <input className="search-field" type="text" name="name" />
        </label>
        <input className="submit-btn" type="submit" value="Submit" />
      </form>
    )
  }
}