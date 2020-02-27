import React from "react";
import PropTypes from "prop-types";

class InstanceTypeIngressRoutedServiceURITable extends React.Component {
    state = {
        add_uri: {
            id: "",
            name: "",
            path: ""
        },
        edit_uri: {
            id: "",
            name: "",
            path: ""
        },
        uris: [],
        uris_loaded: false
    };

    refreshData() {
        fetch("/api/instance-type-ingress-svc-uri?instance_type_svc=" + this.props.instance_type_svc_id)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => this.setState({uris: data, uris_loaded: true}));
    }

    componentDidMount() {
        this.refreshData();
    }

    handleAddURI = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            instance_type_svc: this.props.instance_type_svc_id,
            name: this.state.add_uri.name,
            path: this.state.add_uri.path
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        this.setState({
            add_uri: {
                id: "",
                name: "",
                path: ""
            }
        });
        fetch("/api/instance-type-ingress-svc-uri/new", conf).then(response => {
            this.setState({submitted: true});
            this.refreshData();
        });

    };

    handleEditURISave = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            instance_type_svc: this.state.edit_uri.instance_type_svc,
            name: this.state.edit_uri.name,
            path: this.state.edit_uri.path
        };
        const conf = {
            method: "PUT",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        this.setState({
            edit_uri: {
                id: "",
                name: "",
                path: ""
            }
        });
        fetch("/api/instance-type-ingress-svc-uri/" + this.state.edit_uri.id, conf).then(response => {
            this.setState({submitted: true});
            this.refreshData();
        });
    };

    handleDeleteURI = e => {
        const conf = {
            method: "DELETE",
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/instance-type-ingress-svc-uri/" + e.id, conf).then(response => {
            this.setState({submitted: true});
            this.refreshData();
        });
    };

    cancelEditURI = e => {
        e.preventDefault();
        this.setState({
            edit_uri: {
                id: "",
                name: "",
                path: ""
            }
        })
    };

    handleEditURI = o => {
        console.log('editing ');
        console.log(o);
        this.setState({edit_uri: o})
    };

    handleAddChange = e => {
        let new_state = this.state;
        new_state.add_uri[e.target.name] = e.target.value;
        this.setState(new_state);
    };

    handleEditChange = e => {
        let new_state = this.state;
        new_state.edit_uri[e.target.name] = e.target.value;
        this.setState(new_state);
    };

    render() {
        return (
            <table className="table is-striped">
                <thead>
                <tr>
                    <th>Name</th>
                    <th>Path</th>
                    <th/>
                </tr>
                </thead>
                <tbody>
                {this.state.uris.map(el => (
                    <tr key={el.id}>
                        <td>{this.state.edit_uri.id === el.id ? <input
                            className="input"
                            type="text"
                            name="name"
                            onChange={this.handleEditChange}
                            value={this.state.edit_uri.name}
                            required
                        /> : el.name}</td>
                        <td>{this.state.edit_uri.id === el.id ? <input
                            className="input"
                            type="text"
                            name="path"
                            onChange={this.handleEditChange}
                            value={this.state.edit_uri.path}
                            required
                        /> : el.path}</td>
                        {this.state.edit_uri.id === el.id ?
                            <td>
                                <div className="buttons">
                                    <a className="button" onClick={this.handleEditURISave}>Save</a>
                                    <a className="button" onClick={this.cancelEditURI}>Cancel</a>
                                </div>
                            </td> :
                            <td>
                                <div className="buttons">
                                    <a className="button" onClick={() => this.handleEditURI(el)}>Edit</a>
                                    <a className="button" onClick={() => this.handleDeleteURI(el)}>Delete</a>
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
                            value={this.state.add_uri.name}
                            required
                        />
                    </td>
                    <td>
                        <input
                            className="input"
                            type="text"
                            name="path"
                            onChange={this.handleAddChange}
                            value={this.state.add_uri.path}
                            required
                        />
                    </td>
                    <td>
                        <div className="buttons">
                            <a className="button" onClick={this.handleAddURI}>Add URI</a>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
        );
    }
}

InstanceTypeIngressRoutedServiceURITable.propTypes = {
    instance_type_svc_id: PropTypes.number.isRequired
};

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
                    <React.Fragment key={el.id}>
                        <tr>
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
                        <tr>
                            <td/>
                            <td colSpan="4">
                                <h5>Service URIs</h5>
                                <InstanceTypeIngressRoutedServiceURITable instance_type_svc_id={el.id}/>
                            </td>
                        </tr>
                    </React.Fragment>
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
                            <a className="button" onClick={this.handleAddService}>Add Service</a>
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
