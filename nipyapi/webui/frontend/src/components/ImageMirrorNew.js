import React, {Component} from "react";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, ImageMirrorsCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import {perform_cloud_ops} from "../util/bg_tasks";

export class ImageMirrorNew extends Component {
    state = {
        from_image: "",
        to_image: "",
        auth: ""
    };

    handleSubmit = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            from_image: this.state.from_image,
            to_image: this.state.to_image,
            auth: this.state.auth
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/image-mirror/new", conf).then(response => {
            this.setState({submitted: true});
            perform_cloud_ops();
        });

    };

    handleChange = e => {
        this.setState({[e.target.name]: e.target.value});
    };

    render() {
        if (this.state.submitted) {
            return <Redirect to="/mirror-images" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <ImageMirrorsCrumb/>
                    <CurrentCrumb>New Mirror Image</CurrentCrumb>
                </Breadcrumb>
                <div className="column">
                    <form onSubmit={this.handleSubmit}>
                        <div className="field">
                            <label className="label">From Image</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="from_image"
                                    onChange={this.handleChange}
                                    value={this.state.from_image}
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">To Image</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="to_image"
                                    onChange={this.handleChange}
                                    value={this.state.to_image}
                                    required
                                />
                            </div>
                            <p>Of the form <em>gcr.io/gcp-dim/&lt;your img&gt;</em></p>
                        </div>
                        <div className="field">
                            <label className="label">Docker Auth Config</label>
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
                                    Create Mirror Image
                                </button>
                            )}
                        </div>
                    </form>
                </div>
            </React.Fragment>
        );
    }
}
