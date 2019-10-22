import React, {Component} from "react";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, NifiInstancesCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import {perform_cloud_ops} from "../util/bg_tasks";

export class NifiInstanceNew extends Component {
    state = {
        name: "",
        hostname: "",
        creating: false,
        submitted: false,
        cluster: 0
    };

    handleSubmit = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            name: this.state.name,
            hostname: this.state.hostname,
            cluster: parseInt(this.state.cluster)
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/nifi/new", conf).then(response => {
            this.setState({submitted: true});
            perform_cloud_ops();
        });

    };

    handleChange = e => {
        this.setState({[e.target.name]: e.target.value});
    };

    render() {
        if (this.state.submitted) {
            return <Redirect to="/" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <NifiInstancesCrumb/>
                    <CurrentCrumb>New Instance</CurrentCrumb>
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
                            <label className="label">Hostname</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="hostname"
                                    onChange={this.handleChange}
                                    value={this.state.hostname}
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">K8s Cluster</label>
                            <div className="control">
                                <select name="cluster" value={this.state.cluster} onChange={this.handleChange}>
                                    <option key=""/>
                                    <DataProvider endpoint={"/api/k8s-cluster"}
                                                  placeholder={<React.Fragment/>}
                                                  render={data => data.map(el => (
                                                      <option key={el.id}
                                                              value={el.id}>{el.name}</option>
                                                  ))}/>
                                </select>
                            </div>
                        </div>
                        <div className="control">
                            {this.state.creating ? <span>Creating...</span> : (
                                <button type="submit" className="button is-info">
                                    Create Instance
                                </button>
                            )}
                        </div>
                    </form>
                </div>
            </React.Fragment>
        );
    }
}
