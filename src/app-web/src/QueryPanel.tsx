import React, { Component } from 'react';
import styled from 'styled-components';
import { StyledH1DarkBg } from './Dashboard';

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

  handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    this.setState({ query: event.target.value });
  }

  /**
   * Query submission handler. 
   * 
   * Resets local `query` state; calls parent query state setter to update the 
   * shared `query` state.
   * 
   * @param event: submission related event
   */
  handleSubmit(event: React.FormEvent | React.MouseEvent) {
    if (this.state.query !== "") {
      this.props.setQueryInParent(this.state.query);
      this.setState({ query: "" });
    }
    event.preventDefault();
  }

  render() {
    return (
      <StyledQueryForm onSubmit={this.handleSubmit}>
        <label>
          <StyledH1DarkBg>TV Series</StyledH1DarkBg>
          <StyledSearchFieldInput type="text" name="tv-series"
            value={this.state.query} onChange={this.handleChange}
          />
        </label>
        <StyledSubmitBtn type="submit" disabled={this.state.query === ""} onClick={this.handleSubmit}>
          Search
        </StyledSubmitBtn>
      </StyledQueryForm>
    )
  }
}

const StyledSearchFieldInput = styled.input`
  width: 100%;
  padding: 0.8rem;
  margin: 1.83rem 0 1.2rem;
  box-sizing: border-box;
  border: 0;
  font-size: 1.2rem;
  color: white;
  background: rgb(63, 63, 63);
  border-radius: 0.3rem;

  :focus {
    outline: none;
  }
`;

const StyledSubmitBtn = styled.button`
  background-color: #230fd3;
  border: none;
  color: white;
  padding: 0.9rem 1.8rem;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 1.05rem;
  font-weight: bold;
  border-radius: 0.3rem;
  transition: background 0.5s ease-out;

  :focus {
    outline: none;
  }

  :disabled {
    color: #b5b5b5;
    background-color: #0f056e;
  }
`;

const StyledQueryForm = styled.form`
  padding: 0 2rem;
`;