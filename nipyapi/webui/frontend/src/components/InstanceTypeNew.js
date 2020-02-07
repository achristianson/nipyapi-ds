import React, {Component} from "react";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, DockerAuthConfigsCrumb, InstanceTypesCrumb, NifiImagesCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import {perform_cloud_ops} from "../util/bg_tasks";

export class InstanceTypeNew extends Component {
    state = {
        name: "",
        image: "",
        auth: "",
    };

    handleSubmit = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            name: this.state.name,
            image: this.state.image,
            auth: this.state.auth,
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
                        <div className="field">
                            <label className="label">Docker Registry Auth</label>
                            <div className="control">
                                <select name="auth" value={this.state.auth} onChange={this.handleChange}>
                                    <option key=""/>
                                    <DataProvider endpoint={"/api/docker-registry-auth"}
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
