import React, {Component} from "react";
import PropTypes from "prop-types";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, ImageMirrorsCrumb} from "./Breadcrumb";
import {perform_cloud_ops} from "../util/bg_tasks";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {Link} from "react-router-dom";

export class ImageMirrorDetail extends Component {
    static propTypes = {
        data: PropTypes.object.isRequired
    };

    state = {
        deleted: false
    };

    handleDelete = () => {
        console.log("Requesting deletion of mirror image: " + this.props.data.id);
        fetch("/api/image-mirror/" + this.props.data.id + "", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            if (response.status !== 204) {
                console.log("Failed to request deletion of mirror image: " + this.props.data.id)
            } else {
                console.log("Requested deletion of mirror image: " + this.props.data.id);
                perform_cloud_ops();
            }
        });
        this.setState({deleted: true});
    };

    handleMirror = () => {
        console.log("Requesting build of mirror image: " + this.props.data.id);
        fetch("/api/image-mirror-job/new", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                mirror: this.props.data.id,
                state: 'PENDING_MIRROR'
            })
        }).then(response => {
            if (response.status !== 201) {
                console.log("Failed to request mirror of image: " + this.props.data.id)
            } else {
                console.log("Requested mirror of image: " + this.props.data.id);
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
            return <Redirect to="/mirror-images" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <ImageMirrorsCrumb/>
                    <CurrentCrumb>{this.props.data.from_image}</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <h3>{this.props.data.from_image}</h3>

                        <table className="table is-fullwidth">
                            <tbody>
                            <tr>
                                <td>From Image</td>
                                <td>{this.props.data.from_image}</td>
                            </tr>
                            <tr>
                                <td>To Image</td>
                                <td>{this.props.data.to_image}</td>
                            </tr>
                            </tbody>
                        </table>

                        <h4>Mirror Jobs</h4>

                        <DataProvider endpoint={"/api/image-mirror-job?image=" + this.props.data.id}
                                      placeholder={<p>Loading...</p>}
                                      render={data => <Table data={data.map(d => {
                                          return {
                                              id: d.id,
                                              "Mirror Job ID": d.id,
                                              "State": d.state,
                                              "Docker ID": d.docker_id
                                          }
                                      })}/>} ref="provider"/>

                        <div className="buttons">
                            <a className="button" onClick={this.handleDelete}>Delete Mirror Image</a>
                            <a className="button" onClick={this.handleRefresh}>Refresh</a>
                            <a className="button" onClick={this.handleMirror}>Start Mirror Job</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
