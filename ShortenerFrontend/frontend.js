'use strict';

const e = React.createElement;
console.log('log')

class Frontend extends React.Component {
  constructor(props) {
    super(props);
    this.state = { url: '', message: '', slug: '', desired_slug: '' };

               
    this.response = {};
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleDesiredChange = this.handleDesiredChange.bind(this);
  }

  render() {
     var link;
     
     if (this.state.slug.length > 0) {
       link = <span>http://127.0.0.1:5000/{this.state.slug}</span>
     }
     
      return (
      <div>
        <form onSubmit={this.handleSubmit}>
            <label> Url </label>
            <input type="text" value={this.state.url}  onChange={this.handleChange} /><br/>
            <label> Desired hash </label>
            <input type="text" value={this.state.desired_slug} onChange={this.handleDesiredChange} /><br/>
            <input type="submit" value="Shorten" />
        </form>

        <div>
            {this.state.message}
        </div>
            {link}
       </div>
      );
  }

  handleChange(event) {
    this.setState({
        url: event.target.value
    });
  }

  handleDesiredChange(event) {
    this.setState({ desired_slug: event.target.value});
  }

  handleSubmit(event) {
    const self = this;
    fetch("http://127.0.0.1:5000", {
        method: "POST",
        headers: {
          'content-type': 'application/json'
        },
        body: JSON.stringify(this.state)
       }).then(function(response) {
        response.json().then(data => {
        console.log(data);
            self.setState({
                message: data.message,
                slug: data.slug || ''
            })
        });
       });
    event.preventDefault();
  }
}

const domContainer = document.querySelector('#container');
ReactDOM.render(e(Frontend), domContainer);