import React, {Component} from "react";
import PropTypes from "prop-types";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, DockerAuthConfigsCrumb, InstanceTypesCrumb, NifiImagesCrumb} from "./Breadcrumb";
import {perform_cloud_ops} from "../util/bg_tasks";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {Link} from "react-router-dom";
import InstanceTypeEnvVarTable from "./InstanceTypeEnvVarTable";
import InstanceTypePortTable from "./InstanceTypePortTable";

export class InstanceTypeDetail extends Component {
    static propTypes = {
        data: PropTypes.object.isRequired
    };

    state = {
        deleted: false
    };

    handleDelete = () => {
        console.log("Requesting deletion of instance type: " + this.props.data.id);
        fetch("/api/instance-type/" + this.props.data.id + "", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            if (response.status !== 204) {
                console.log("Failed to request deletion of instance type: " + this.props.data.id)
            } else {
                console.log("Requested deletion of instance type: " + this.props.data.id);
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
                    <CurrentCrumb>{this.props.data.name}</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <h3>{this.props.data.name}</h3>

                        <table className="table is-fullwidth">
                            <tbody>
                            <tr>
                                <td>Name</td>
                                <td>{this.props.data.name}</td>
                            </tr>
                            <tr>
                                <td>Container Name</td>
                                <td>{this.props.data.container_name}</td>
                            </tr>
                            <tr>
                                <td>Docker Image</td>
                                <td>{this.props.data.image}</td>
                            </tr>
                            </tbody>
                        </table>

                        <h4>Environment Variables</h4>

                        <InstanceTypeEnvVarTable instance_type_id={this.props.data.id}/>

                        <h4>Ports</h4>

                        <InstanceTypePortTable instance_type_id={this.props.data.id}/>

                        <div className="buttons">
                            <a className="button" onClick={this.handleDelete}>Delete Instance Type</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
