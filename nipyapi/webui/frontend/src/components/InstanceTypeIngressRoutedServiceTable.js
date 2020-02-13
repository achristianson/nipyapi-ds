import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import {perform_cloud_ops} from "../util/bg_tasks";

class InstanceTypeIngressRoutedServiceTable extends React.Component {
    state = {
        add_service: {
            id: "",
            name: "",
            service_name: "",
            svc_port: "",
            target_port: ""
        },
        edit_service: {
            id: "",
            name: "",
            service_name: "",
            svc_port: "",
            target_port: ""
        },
        services: [],
        services_loaded: false
    };

    refreshServices() {
        fetch("/api/instance-type-ingress-svc?instance_type=" + this.props.instance_type_id)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => this.setState({services: data, services_loaded: true}));
    }

    componentDidMount() {
        this.refreshServices();
    }

    handleAddService = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            instance_type: this.props.instance_type_id,
            name: this.state.add_service.name,
            service_name: this.state.add_service.service_name,
            svc_port: this.state.add_service.svc_port,
            target_port: this.state.add_service.target_port
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        this.setState({
            add_service: {
                id: "",
                name: "",
                service_name: "",
                svc_port: "",
                target_port: ""
            }
        });
        fetch("/api/instance-type-ingress-svc/new", conf).then(response => {
            this.setState({submitted: true});
            this.refreshServices();
        });

    };

    handleEditServiceSave = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            instance_type: this.state.edit_service.instance_type,
            name: this.state.edit_service.name,
            service_name: this.state.edit_service.service_name,
            svc_port: this.state.edit_service.svc_port,
            target_port: this.state.edit_service.target_port
        };
        const conf = {
            method: "PUT",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        this.setState({
            edit_service: {
                id: "",
                name: "",
                service_name: "",
                svc_port: "",
                target_port: ""
            }
        });
        fetch("/api/instance-type-ingress-svc/" + this.state.edit_service.id, conf).then(response => {
            this.setState({submitted: true});
            this.refreshServices();
        });

    };

    handleDeleteService = e => {
        const conf = {
            method: "DELETE",
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/instance-type-ingress-svc/" + e.id, conf).then(response => {
            this.setState({submitted: true});
            this.refreshServices();
        });
    };

    cancelEditService = e => {
        e.preventDefault();
        this.setState({
            edit_service: {
                id: "",
                name: "",
                service_name: "",
                svc_port: "",
                target_port: ""
            }
        })
    };

    handleEditService = e => {
        console.log('editing ');
        console.log(e);
        this.setState({edit_service: e})
    };

    handleAddChange = e => {
        let new_state = this.state;
        new_state.add_service[e.target.name] = e.target.value;
        this.setState(new_state);
    };

    handleEditChange = e => {
        let new_state = this.state;
        new_state.edit_service[e.target.name] = e.target.value;
        this.setState(new_state);
    };

    render() {
        return (
            <table className="table is-striped">
                <thead>
                <tr>
                    <th>Name</th>
                    <th>DNS Name</th>
                    <th>Target Port</th>
                    <th>Service Port</th>
                    <th/>
                </tr>
                </thead>
                <tbody>
                {this.state.services.map(el => (
                    <tr key={el.id}>
                        <td>{this.state.edit_service.id === el.id ? <input
                            className="input"
                            type="text"
                            name="name"
                            onChange={this.handleEditChange}
                            value={this.state.edit_service.name}
                            required
                        /> : el.name}</td>
                        <td>{this.state.edit_service.id === el.id ? <input
                            className="input"
                            type="text"
                            name="service_name"
                            onChange={this.handleEditChange}
                            value={this.state.edit_service.service_name}
                            required
                        /> : el.service_name}</td>
                        <td>{this.state.edit_service.id === el.id ? <input
                            className="input"
                            type="text"
                            name="target_port"
                            onChange={this.handleEditChange}
                            value={this.state.edit_service.target_port}
                            required
                        /> : el.target_port}</td>
                        <td>{this.state.edit_service.id === el.id ? <input
                            className="input"
                            type="text"
                            name="svc_port"
                            onChange={this.handleEditChange}
                            value={this.state.edit_service.svc_port}
                            required
                        /> : el.svc_port}</td>
                        {this.state.edit_service.id === el.id ?
                            <td>
                                <div className="buttons">
                                    <a className="button" onClick={this.handleEditServiceSave}>Save</a>
                                    <a className="button" onClick={this.cancelEditService}>Cancel</a>
                                </div>
                            </td> :
                            <td>
                                <div className="buttons">
                                    <a className="button" onClick={() => this.handleEditService(el)}>Edit</a>
                                    <a className="button" onClick={() => this.handleDeleteService(el)}>Delete</a>
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
                            value={this.state.add_service.name}
                            required
                        />
                    </td>
                    <td>
                        <input
                            className="input"
                            type="text"
                            name="service_name"
                            onChange={this.handleAddChange}
                            value={this.state.add_service.service_name}
                            required
                        />
                    </td>
                    <td>
                        <input
                            className="input"
                            type="text"
                            name="target_port"
                            onChange={this.handleAddChange}
                            value={this.state.add_service.target_port}
                            required
                        />
                    </td>
                    <td>
                        <input
                            className="input"
                            type="text"
                            name="svc_port"
                            onChange={this.handleAddChange}
                            value={this.state.add_service.svc_port}
                            required
                        />
                    </td>
                    <td>
                        <div className="buttons">
                            <a className="button" onClick={this.handleAddService}>Add</a>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
        );
    }
}

InstanceTypeIngressRoutedServiceTable.propTypes = {
    instance_type_id: PropTypes.number.isRequired
};

export default InstanceTypeIngressRoutedServiceTable;
