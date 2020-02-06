import React, {Component} from "react";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, DockerAuthConfigsCrumb, NifiImagesCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import {perform_cloud_ops} from "../util/bg_tasks";

export class DockerAuthConfigNew extends Component {
    state = {
        name: "",
        username: "",
        password: ""
    };

    handleSubmit = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            name: this.state.name,
            username: this.state.username,
            password: this.state.password
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/docker-registry-auth/new", conf).then(response => {
            this.setState({submitted: true});
            perform_cloud_ops();
        });

    };

    handleChange = e => {
        this.setState({[e.target.name]: e.target.value});
    };

    render() {
        if (this.state.submitted) {
            return <Redirect to="/docker-auth-configs" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <DockerAuthConfigsCrumb/>
                    <CurrentCrumb>New Docker Auth Config</CurrentCrumb>
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
                            <label className="label">Username</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="username"
                                    onChange={this.handleChange}
                                    value={this.state.username}
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Password</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="password"
                                    name="password"
                                    onChange={this.handleChange}
                                    value={this.state.password}
                                    required
                                />
                            </div>
                        </div>
                        <div className="control">
                            {this.state.creating ? <span>Creating...</span> : (
                                <button type="submit" className="button is-info">
                                    Create Config
                                </button>
                            )}
                        </div>
                    </form>
                </div>
            </React.Fragment>
        );
    }
}
