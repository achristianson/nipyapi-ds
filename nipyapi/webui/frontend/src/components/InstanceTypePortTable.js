import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import {perform_cloud_ops} from "../util/bg_tasks";

class InstanceTypePortTable extends React.Component {
    state = {
        add_port: {
            id: "",
            internal: "",
            external: ""
        },
        edit_port: {
            id: "",
            internal: "",
            external: ""
        },
        ports: [],
        ports_loaded: false
    };

    refreshPorts() {
        fetch("/api/instance-type-port?instance_type=" + this.props.instance_type_id)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => this.setState({ports: data, ports_loaded: true}));
    }

    componentDidMount() {
        this.refreshPorts();
    }

    handleAddPort = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            instance_type: this.props.instance_type_id,
            internal: this.state.add_port.internal,
            external: this.state.add_port.external
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        this.setState({
            add_port: {
                id: "",
                internal: "",
                external: ""
            }
        });
        fetch("/api/instance-type-port/new", conf).then(response => {
            this.setState({submitted: true});
            this.refreshPorts();
        });

    };

    handleEditPortSave = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            instance_type: this.state.edit_port.instance_type,
            internal: this.state.edit_port.internal,
            external: this.state.edit_port.external
        };
        const conf = {
            method: "PUT",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        this.setState({
            edit_port: {
                id: "",
                internal: "",
                external: ""
            }
        });
        fetch("/api/instance-type-port/" + this.state.edit_port.id, conf).then(response => {
            this.setState({submitted: true});
            this.refreshPorts();
        });

    };

    handleDeletePort = e => {
        const conf = {
            method: "DELETE",
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/instance-type-port/" + e.id, conf).then(response => {
            this.setState({submitted: true});
            this.refreshPorts();
        });
    };

    cancelEditPort = e => {
        e.preventDefault();
        this.setState({
            edit_port: {
                id: "",
                internal: "",
                external: ""
            }
        })
    };

    handleEditPort = e => {
        console.log('editing ');
        console.log(e);
        this.setState({edit_port: e})
    };

    handleAddChange = e => {
        let new_state = this.state;
        new_state.add_port[e.target.name] = e.target.value;
        this.setState(new_state);
    };

    handleEditChange = e => {
        let new_state = this.state;
        new_state.edit_port[e.target.name] = e.target.value;
        this.setState(new_state);
    };

    render() {
        return (
            <table className="table is-striped">
                <thead>
                <tr>
                    <th>Internal</th>
                    <th>External</th>
                    <th/>
                </tr>
                </thead>
                <tbody>
                {this.state.ports.map(el => (
                    <tr key={el.id}>
                        <td>{this.state.edit_port.id === el.id ? <input
                            className="input"
                            type="text"
                            name="internal"
                            onChange={this.handleEditChange}
                            value={this.state.edit_port.internal}
                            required
                        /> : el.internal}</td>
                        <td>{this.state.edit_port.id === el.id ? <input
                            className="input"
                            type="text"
                            name="external"
                            onChange={this.handleEditChange}
                            value={this.state.edit_port.external}
                            required
                        /> : el.external}</td>
                        {this.state.edit_port.id === el.id ?
                            <td>
                                <div className="buttons">
                                    <a className="button" onClick={this.handleEditPortSave}>Save</a>
                                    <a className="button" onClick={this.cancelEditPort}>Cancel</a>
                                </div>
                            </td> :
                            <td>
                                <div className="buttons">
                                    <a className="button" onClick={() => this.handleEditPort(el)}>Edit</a>
                                    <a className="button" onClick={() => this.handleDeletePort(el)}>Delete</a>
                                </div>
                            </td>}
                    </tr>
                ))}
                <tr>
                    <td>
                        <input
                            className="input"
                            type="text"
                            name="internal"
                            onChange={this.handleAddChange}
                            value={this.state.add_port.internal}
                            required
                        />
                    </td>
                    <td>
                        <input
                            className="input"
                            type="text"
                            name="external"
                            onChange={this.handleAddChange}
                            value={this.state.add_port.external}
                            required
                        />
                    </td>
                    <td>
                        <div className="buttons">
                            <a className="button" onClick={this.handleAddPort}>Add</a>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
        );
    }
}

InstanceTypePortTable.propTypes = {
    instance_type_id: PropTypes.number.isRequired
};

export default InstanceTypePortTable;
