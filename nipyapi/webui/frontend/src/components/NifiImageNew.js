import React, {Component} from "react";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, NifiImagesCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import {perform_cloud_ops} from "../util/bg_tasks";

export class NifiImageNew extends Component {
    state = {
        git_repo: "",
        branch: "",
        mvn_build_args: "-T8 -DskipTests=true clean package",
        tag: ""
    };

    handleSubmit = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            git_repo: this.state.git_repo,
            branch: this.state.branch,
            mvn_build_args: this.state.mvn_build_args,
            tag: this.state.tag
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/nifi-image/new", conf).then(response => {
            this.setState({submitted: true});
            perform_cloud_ops();
        });

    };

    handleChange = e => {
        this.setState({[e.target.name]: e.target.value});
    };

    render() {
        if (this.state.submitted) {
            return <Redirect to="/nifi-images" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <NifiImagesCrumb/>
                    <CurrentCrumb>New NiFi Image</CurrentCrumb>
                </Breadcrumb>
                <div className="column">
                    <form onSubmit={this.handleSubmit}>
                        <div className="field">
                            <label className="label">Git Repo</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="git_repo"
                                    onChange={this.handleChange}
                                    value={this.state.git_repo}
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Branch</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="branch"
                                    onChange={this.handleChange}
                                    value={this.state.branch}
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Maven Build Arguments</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="mvn_build_args"
                                    onChange={this.handleChange}
                                    value={this.state.mvn_build_args}
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Docker Image Tag</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="tag"
                                    onChange={this.handleChange}
                                    value={this.state.tag}
                                    required
                                />
                            </div>
                        </div>
                        <div className="control">
                            {this.state.creating ? <span>Creating...</span> : (
                                <button type="submit" className="button is-info">
                                    Create Image
                                </button>
                            )}
                        </div>
                    </form>
                </div>
            </React.Fragment>
        );
    }
}
