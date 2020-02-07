import React, {Component} from "react";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, NifiInstancesCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import {perform_cloud_ops} from "../util/bg_tasks";

export class NifiInstanceNew extends Component {
    state = {
        name: "",
        image: "apache/nifi:latest",
        hostname: "",
        namespace: "",
        deploy_mongo: false,
        deploy_kafka: false,
        deploy_prometheus: false,
        deploy_jupyter: false,
        creating: false,
        submitted: false,
        instance_types: [],
        instance_types_loaded: false,
        cluster: 0
    };

    refreshInstanceTypes() {
        fetch("/api/instance-type")
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => this.setState({
                instance_types: data.map(o => Object.assign(o, {checked: false, saved: false})),
                instance_types_loaded: true
            }));
    }

    componentDidMount() {
        this.refreshInstanceTypes();
    }

    handleSubmit = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            name: this.state.name,
            image: this.state.image,
            hostname: this.state.hostname,
            cluster: parseInt(this.state.cluster),
            namespace: this.state.namespace,
            deploy_mongo: this.state.deploy_mongo,
            deploy_kafka: this.state.deploy_kafka,
            deploy_prometheus: this.state.deploy_prometheus,
            deploy_jupyter: this.state.deploy_jupyter
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/nifi/new", conf)
            .then(r => r.json())
            .then(new_inst => {
                console.log('successfully created instance; adding component instances');
                this.state.instance_types.forEach(instance_type => {
                    if (instance_type.checked) {
                        console.log('adding instance: ' + instance_type.name);
                        fetch("/api/instance/new", {
                            method: "POST",
                            headers: new Headers({"Content-Type": "application/json"}),
                            body: JSON.stringify({
                                instance_type: instance_type.id,
                                parent: new_inst.id
                            })
                        }).then(response => {
                            let new_state = this.state;
                            new_state.instance_types.map(o => Object.assign(o, {saved: instance_type.id === o.id}));
                            this.setState(new_state);
                            const is_complete = new_state.instance_types.reduce((acc, cur) => acc && cur.saved, true);
                            if (is_complete) {
                                console.log("completed adding component instances");
                                this.setState({submitted: true});
                                perform_cloud_ops();
                            }
                        })
                    }
                });
            });

    };

    handleChange = e => {
        if (e.target.name === "deploy_mongo" ||
            e.target.name === "deploy_kafka" ||
            e.target.name === "deploy_prometheus" ||
            e.target.name === "deploy_jupyter") {
            if (e.target.checked) {
                this.setState({[e.target.name]: true});
            } else {
                this.setState({[e.target.name]: false});
            }
        } else {
            this.setState({[e.target.name]: e.target.value});
        }
    };

    handleInstanceTypeChecked = e => {
        let new_state = this.state;
        new_state.instance_types.map(o => Object.assign(o, {checked: e.checked ? e.id !== o.id : e.id === o.id}));
        this.setState(new_state);
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
                            <label className="label">Hostname</label>
                            <div className="control">
                                <div className="columns">
                                    <div className="column is-one-quarter">
                                        <input
                                            className="input"
                                            type="text"
                                            name="hostname"
                                            onChange={this.handleChange}
                                            value={this.state.hostname}
                                            style={{textAlign: 'right'}}
                                            required
                                        />
                                    </div>
                                    <div className="column">
                                        <div className="field">
                                            <label className="label">{' '}</label>
                                            <div className="control">
                                                {window.nifi_web_config ? '.' + window.nifi_web_config.domain : ''}
                                            </div>
                                        </div>

                                    </div>
                                </div>
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
                        <div className="field">
                            <label className="label">Namespace</label>
                            <div className="control">
                                <input
                                    className="input"
                                    type="text"
                                    name="namespace"
                                    onChange={this.handleChange}
                                    value={this.state.namespace}
                                    required
                                />
                            </div>
                        </div>
                        <div className="field"><strong>Additional Components</strong></div>
                        <div className="field">
                            <div>
                                <label className="checkbox">
                                    <input type="checkbox"
                                           name="deploy_mongo"
                                           checked={this.state.deploy_mongo}
                                           onChange={this.handleChange}/>
                                    {` `}Deploy Mongo
                                </label>
                            </div>
                        </div>
                        <div className="field">
                            <div>
                                <label className="checkbox">
                                    <input type="checkbox"
                                           name="deploy_kafka"
                                           checked={this.state.deploy_kafka}
                                           onChange={this.handleChange}/>
                                    {` `}Deploy Kafka
                                </label>
                            </div>
                        </div>
                        <div className="field">
                            <div>
                                <label className="checkbox">
                                    <input type="checkbox"
                                           name="deploy_prometheus"
                                           checked={this.state.deploy_prometheus}
                                           onChange={this.handleChange}/>
                                    {` `}Deploy Prometheus
                                </label>
                            </div>
                        </div>
                        <div className="field">
                            <div>
                                <label className="checkbox">
                                    <input type="checkbox"
                                           name="deploy_jupyter"
                                           checked={this.state.deploy_jupyter}
                                           onChange={this.handleChange}/>
                                    {` `}Deploy Jupyter Notebook Data Science Stack
                                </label>
                            </div>
                        </div>
                        {this.state.instance_types.map(instance_type =>
                            <div key={instance_type.id} className="field">
                                <div>
                                    <label className="checkbox">
                                        <input type="checkbox"
                                               name="deploy_type"
                                               checked={instance_type.checked}
                                               onChange={() => this.handleInstanceTypeChecked(instance_type)}/>
                                        {` `}Deploy {instance_type.name}
                                    </label>
                                </div>
                            </div>)}
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
