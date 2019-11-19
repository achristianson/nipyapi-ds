import React, {Component} from "react";
import PropTypes from "prop-types";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, NifiImagesCrumb} from "./Breadcrumb";
import {perform_cloud_ops} from "../util/bg_tasks";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {Link} from "react-router-dom";

export class NifiImageDetail extends Component {
    static propTypes = {
        data: PropTypes.object.isRequired
    };

    state = {
        deleted: false
    };

    handleDelete = () => {
        console.log("Requesting deletion of nifi image: " + this.props.data.id);
        fetch("/api/nifi-image/" + this.props.data.id + "", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            if (response.status !== 204) {
                console.log("Failed to request deletion of nifi image: " + this.props.data.id)
            } else {
                console.log("Requested deletion of nifi image: " + this.props.data.id);
                perform_cloud_ops();
            }
        });
        this.setState({deleted: true});
    };

    handleBuild = () => {
        console.log("Requesting build of nifi image: " + this.props.data.id);
        fetch("/api/nifi-image-build/new", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                image: this.props.data.id,
                state: 'PENDING_BUILD'
            })
        }).then(response => {
            if (response.status !== 201) {
                console.log("Failed to request build of nifi image: " + this.props.data.id)
            } else {
                console.log("Requested build of nifi image: " + this.props.data.id);
                this.refs.provider.refresh();
                perform_cloud_ops();
            }
        });
    };

    handleRefresh = () => {
        this.refs.provider.refresh();
    };

    render() {
        if (this.state.deleted) {
            return <Redirect to="/nifi-images" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <NifiImagesCrumb/>
                    <CurrentCrumb>{this.props.data.tag}</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <h3>{this.props.data.tag}</h3>

                        <table className="table is-fullwidth">
                            <tbody>
                            <tr>
                                <td>Git Repo</td>
                                <td>{this.props.data.git_repo}</td>
                            </tr>
                            <tr>
                                <td>Branch</td>
                                <td>{this.props.data.branch}</td>
                            </tr>
                            <tr>
                                <td>Maven Build Arguments</td>
                                <td style={{fontFamily: 'monospace'}}>{this.props.data.mvn_build_args}</td>
                            </tr>
                            <tr>
                                <td>Docker Image Tag</td>
                                <td>{this.props.data.tag}</td>
                            </tr>
                            </tbody>
                        </table>

                        <h4>Builds</h4>

                        <DataProvider endpoint={"/api/nifi-image-build?image=" + this.props.data.id}
                                      placeholder={<p>Loading...</p>}
                                      render={data => <Table data={data.map(d => {
                                          return {
                                              id: d.id,
                                              "Build ID": <Link to={"/nifi-image-build/" + d.id}>{d.id}</Link>,
                                              "State": d.state,
                                              "Docker ID": d.docker_id
                                          }
                                      })}/>} ref="provider"/>

                        <div className="buttons">
                            <a className="button" onClick={this.handleDelete}>Delete Image</a>
                            <a className="button" onClick={this.handleRefresh}>Refresh</a>
                            <a className="button" onClick={this.handleBuild}>Build</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
