import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import {perform_cloud_ops} from "../util/bg_tasks";

class InstanceTypeEnvVarTable extends React.Component {
    state = {
        add_env_var: {
            id: "",
            name: "",
            default_value: ""
        },
        edit_env_var: {
            id: "",
            name: "",
            default_value: ""
        },
        env_vars: [],
        env_vars_loaded: false
    };

    refreshEnvVars() {
        fetch("/api/instance-type-env-var?instance_type=" + this.props.instance_type_id)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => this.setState({env_vars: data, env_vars_loaded: true}));
    }

    componentDidMount() {
        this.refreshEnvVars();
    }

    handleAddVar = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            instance_type: this.props.instance_type_id,
            name: this.state.add_env_var.name,
            default_value: this.state.add_env_var.default_value
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        this.setState({
            add_env_var: {
                id: "",
                name: "",
                default_value: ""
            }
        });
        fetch("/api/instance-type-env-var/new", conf).then(response => {
            this.setState({submitted: true});
            this.refreshEnvVars();
        });

    };

    handleEditVarSave = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            instance_type: this.state.edit_env_var.instance_type,
            name: this.state.edit_env_var.name,
            default_value: this.state.edit_env_var.default_value
        };
        const conf = {
            method: "PUT",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        this.setState({
            edit_env_var: {
                id: "",
                name: "",
                default_value: ""
            }
        });
        fetch("/api/instance-type-env-var/" + this.state.edit_env_var.id, conf).then(response => {
            this.setState({submitted: true});
            this.refreshEnvVars();
        });

    };

    handleDeleteVar = e => {
        const conf = {
            method: "DELETE",
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/instance-type-env-var/" + e.id, conf).then(response => {
            this.setState({submitted: true});
            this.refreshEnvVars();
        });
    };

    cancelEditVar = e => {
        e.preventDefault();
        this.setState({
            edit_env_var: {
                id: "",
                name: "",
                default_value: ""
            }
        })
    };

    handleEditVar = e => {
        console.log('editing ');
        console.log(e);
        this.setState({edit_env_var: e})
    };

    handleAddChange = e => {
        let new_state = this.state;
        new_state.add_env_var[e.target.name] = e.target.value;
        this.setState(new_state);
    };

    handleEditChange = e => {
        let new_state = this.state;
        new_state.edit_env_var[e.target.name] = e.target.value;
        this.setState(new_state);
    };

    render() {
        return (
            <table className="table is-striped">
                <thead>
                <tr>
                    <th>Name</th>
                    <th>Default Value</th>
                    <th/>
                </tr>
                </thead>
                <tbody>
                {this.state.env_vars.map(el => (
                    <tr key={el.id}>
                        <td>{this.state.edit_env_var.id === el.id ? <input
                            className="input"
                            type="text"
                            name="name"
                            onChange={this.handleEditChange}
                            value={this.state.edit_env_var.name}
                            required
                        /> : el.name}</td>
                        <td>{this.state.edit_env_var.id === el.id ? <input
                            className="input"
                            type="text"
                            name="default_value"
                            onChange={this.handleEditChange}
                            value={this.state.edit_env_var.default_value}
                            required
                        /> : el.default_value}</td>
                        {this.state.edit_env_var.id === el.id ?
                            <td>
                                <div className="buttons">
                                    <a className="button" onClick={this.handleEditVarSave}>Save</a>
                                    <a className="button" onClick={this.cancelEditVar}>Cancel</a>
                                </div>
                            </td> :
                            <td>
                                <div className="buttons">
                                    <a className="button" onClick={() => this.handleEditVar(el)}>Edit</a>
                                    <a className="button" onClick={() => this.handleDeleteVar(el)}>Delete</a>
                                </div>
                            </td>}
                    </tr>
                ))}
                <tr>
                    <td>
                        <input
                            className="input"
                            type="text"
                            name="name"
                            onChange={this.handleAddChange}
                            value={this.state.add_env_var.name}
                            required
                        />
                    </td>
                    <td>
                        <input
                            className="input"
                            type="text"
                            name="default_value"
                            onChange={this.handleAddChange}
                            value={this.state.add_env_var.default_value}
                            required
                        />
                    </td>
                    <td>
                        <div className="buttons">
                            <a className="button" onClick={this.handleAddVar}>Add</a>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
        );
    }
}

InstanceTypeEnvVarTable.propTypes = {
    instance_type_id: PropTypes.number.isRequired
};

export default InstanceTypeEnvVarTable;
