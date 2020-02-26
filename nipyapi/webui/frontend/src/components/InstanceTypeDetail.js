import React, {Component} from "react";
import PropTypes from "prop-types";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, InstanceTypesCrumb} from "./Breadcrumb";
import {perform_cloud_ops} from "../util/bg_tasks";
import InstanceTypeEnvVarTable from "./InstanceTypeEnvVarTable";
import InstanceTypePortTable from "./InstanceTypePortTable";
import InstanceTypeIngressRoutedServiceTable from "./InstanceTypeIngressRoutedServiceTable";

export class InstanceTypeDetail extends Component {
    static propTypes = {
        data: PropTypes.object.isRequired
    };

    state = {
        instance_type: {},
        deleted: false,
        editing_name: false,
        editing_container_name: false,
        editing_image: false
    };

    componentDidMount() {
        this.setState({instance_type: this.props.data})
    }

    handleEditName = e => {
        e.preventDefault();
        this.setState({editing_name: true})
    };

    handleCancelEditName = e => {
        e.preventDefault();
        this.setState({editing_name: false})
    };

    handleEditContainerName = e => {
        e.preventDefault();
        this.setState({editing_container_name: true})
    };

    handleCancelEditContainerName = e => {
        e.preventDefault();
        this.setState({editing_container_name: false})
    };

    handleSave = e => {
        e.preventDefault();
        const conf = {
            method: "PUT",
            body: JSON.stringify(this.state.instance_type),
            headers: new Headers({"Content-Type": "application/json"})
        };
        console.log('saving instance type');
        fetch("/api/instance-type/" + this.state.instance_type.id, conf).then(response => {
            console.log('saved instance type');
            this.setState({
                editing_name: false,
                editing_container_name: false,
                editing_image: false
            });
        });

    };

    handleEditChange = e => {
        let new_state = this.state;
        new_state.instance_type[e.target.name] = e.target.value;
        this.setState(new_state);
    };

    handleDelete = () => {
        console.log("Requesting deletion of instance type: " + this.state.instance_type.id);
        fetch("/api/instance-type/" + this.state.instance_type.id + "", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            if (response.status !== 204) {
                console.log("Failed to request deletion of instance type: " + this.state.instance_type.id)
            } else {
                console.log("Requested deletion of instance type: " + this.state.instance_type.id);
                perform_cloud_ops();
            }
        });
        this.setState({deleted: true});
    };

    handleRefresh = () => {
        this.refs.provider.refresh();
    };

    render() {
        if (this.state.deleted) {
            return <Redirect to="/instance-types" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <InstanceTypesCrumb/>
                    <CurrentCrumb>{this.state.instance_type.name}</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <h3>{this.state.instance_type.name}</h3>

                        <table className="table is-fullwidth">
                            <tbody>
                            <tr>
                                <td>Name</td>
                                <td>
                                    {this.state.editing_name ? <input
                                        className="input"
                                        type="text"
                                        name="name"
                                        onChange={this.handleEditChange}
                                        value={this.state.instance_type.name}
                                        required
                                    /> : this.state.instance_type.name}
                                </td>
                                <td>
                                    {this.state.editing_name ?
                                        <div className="buttons">
                                            <a className="button" onClick={this.handleSave}>Save</a>
                                            <a className="button" onClick={this.handleCancelEditName}>Cancel</a>
                                        </div> :
                                        <div className="buttons">
                                            <a className="button" onClick={this.handleEditName}>Edit</a>
                                        </div>}
                                </td>
                            </tr>
                            <tr>
                                <td>Container Name</td>
                                <td>
                                    {this.state.editing_container_name ? <input
                                        className="input"
                                        type="text"
                                        name="container_name"
                                        onChange={this.handleEditChange}
                                        value={this.state.instance_type.container_name}
                                        required
                                    /> : this.state.instance_type.container_name}
                                </td>
                                <td>
                                    {this.state.editing_container_name ?
                                        <div className="buttons">
                                            <a className="button" onClick={this.handleSave}>Save</a>
                                            <a className="button"
                                               onClick={this.handleCancelEditContainerName}>Cancel</a>
                                        </div> :
                                        <div className="buttons">
                                            <a className="button" onClick={this.handleEditContainerName}>Edit</a>
                                        </div>}
                                </td>
                            </tr>
                            <tr>
                                <td>Docker Image</td>
                                <td>{this.state.instance_type.image}</td>
                                <td>
                                    <div className="buttons">
                                        <a className="button" onClick={() => this.handleEditDockerImage()}>Edit</a>
                                    </div>
                                </td>
                            </tr>
                            </tbody>
                        </table>

                        <h4>Environment Variables</h4>

                        <InstanceTypeEnvVarTable instance_type_id={this.props.data.id}/>

                        <h4>Ports</h4>

                        <InstanceTypePortTable instance_type_id={this.props.data.id}/>

                        <h4>Ingress Routed Services</h4>

                        <p>These services are made available to clients outside of the cluster via a global DNS
                            name.</p>

                        <InstanceTypeIngressRoutedServiceTable instance_type_id={this.props.data.id}/>

                        <div className="buttons">
                            <a className="button" onClick={this.handleDelete}>Delete Instance Type</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
