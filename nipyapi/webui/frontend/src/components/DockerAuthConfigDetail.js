import React, {Component} from "react";
import PropTypes from "prop-types";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, DockerAuthConfigsCrumb, NifiImagesCrumb} from "./Breadcrumb";
import {perform_cloud_ops} from "../util/bg_tasks";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {Link} from "react-router-dom";

export class DockerAuthConfigDetail extends Component {
    static propTypes = {
        data: PropTypes.object.isRequired
    };

    state = {
        deleted: false
    };

    handleDelete = () => {
        console.log("Requesting deletion of auth config: " + this.props.data.id);
        fetch("/api/docker-registry-auth/" + this.props.data.id + "", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            if (response.status !== 204) {
                console.log("Failed to request deletion of auth config: " + this.props.data.id)
            } else {
                console.log("Requested deletion of auth config: " + this.props.data.id);
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
            return <Redirect to="/docker-auth-configs" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <DockerAuthConfigsCrumb/>
                    <CurrentCrumb>{this.props.data.name}</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <h3>{this.props.data.name}</h3>

                        <table className="table is-fullwidth">
                            <tbody>
                            <tr>
                                <td>Username</td>
                                <td>{this.props.data.username}</td>
                            </tr>
                            <tr>
                                <td>Password</td>
                                <td>{this.props.data.password.replace(/./g, '•')}</td>
                            </tr>
                            </tbody>
                        </table>


                        <div className="buttons">
                            <a className="button" onClick={this.handleDelete}>Delete Config</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
