import React, {Component} from "react";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, DockerAuthConfigsCrumb, InstanceTypesCrumb, NifiImagesCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import {perform_cloud_ops} from "../util/bg_tasks";

export class InstanceTypeNew extends Component {
    state = {
        name: "",
        container_name: "",
        image: "",
    };

    handleSubmit = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            name: this.state.name,
            container_name: this.state.container_name,
            image: this.state.image,
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/instance-type/new", conf).then(response => {
            this.setState({submitted: true});
            perform_cloud_ops();
        });

    };

    handleChange = e => {
        this.setState({[e.target.name]: e.target.value});
    };

    render() {
        if (this.state.submitted) {
            return <Redirect to="/instance-types" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <InstanceTypesCrumb/>
                    <CurrentCrumb>New Instance Type</CurrentCrumb>
                </Breadcrumb>
                <div className="column">
                    <form onSubmit={this.handleSubmit}>
                        <div className="field">
                            <label className="label">Name</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="name"
                                    onChange={this.handleChange}
                                    value={this.state.name}
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Container Name</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="container_name"
                                    onChange={this.handleChange}
                                    value={this.state.container_name}
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Image</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="image"
                                    onChange={this.handleChange}
                                    value={this.state.image}
                                    required
                                />
                            </div>
                        </div>
                        <div className="control">
                            {this.state.creating ? <span>Creating...</span> : (
                                <button type="submit" className="button is-info">
                                    Create Instance Type
                                </button>
                            )}
                        </div>
                    </form>
                </div>
            </React.Fragment>
        );
    }
}
