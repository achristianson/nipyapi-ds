import React, {Component} from "react";
import PropTypes from "prop-types";

class DataProvider extends Component {
    static propTypes = {
        endpoint: PropTypes.string.isRequired,
        render: PropTypes.func.isRequired,
        placeholder: PropTypes.element.isRequired
    };

    state = {
        data: [],
        loaded: false
    };

    refresh() {
        fetch(this.props.endpoint)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => this.setState({data: data, loaded: true}));
    }

    componentDidMount() {
        this.refresh();
    }

    render() {
        const {data, loaded} = this.state;
        return loaded ? this.props.render(data) : <React.Fragment>{this.props.placeholder}</React.Fragment>;
    }
}

export default DataProvider;
