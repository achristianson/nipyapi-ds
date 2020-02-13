import React, {Component} from "react";
import PropTypes from "prop-types";
import {Redirect} from "react-router";
import {Breadcrumb, CurrentCrumb, NifiInstancesCrumb} from "./Breadcrumb";
import {ClusterMini} from "./ClusterMini";
import {perform_cloud_ops} from "../util/bg_tasks";


class InstanceSvcRow extends Component {
    static propTypes = {
        service: PropTypes.object.isRequired,
        nifi_instance: PropTypes.object.isRequired
    };

    state = {};

    render() {
        return <tr>
            <td>{this.props.service.name}</td>
            <td>
                <a
                    target="_blank"
                    href={"https://" + this.props.service.service_name + "-" + this.props.nifi_instance.hostname + "." + window.nifi_web_config.domain + "/"}>
                    {"https://" + this.props.service.service_name + "-" + this.props.nifi_instance.hostname + "." + window.nifi_web_config.domain}
                </a></td>
        </tr>;
    }
}


class InstanceRow extends Component {
    static propTypes = {
        instance: PropTypes.number.isRequired,
        nifi_instance: PropTypes.object.isRequired
    };

    state = {
        services_loaded: false,
        services: []
    };

    refreshServices() {
        fetch("/api/instance-type-ingress-svc?parent=" + this.props.instance.instance_type)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => this.setState({services: data, services_loaded: true}));
    }

    componentDidMount() {
        this.refreshServices();
    }

    render() {
        return this.state.services_loaded ? this.state.services.map(service => <InstanceSvcRow key={service.id} service={service} nifi_instance={this.props.nifi_instance}/>) :
            <tr>
                <td/>
                <td>Loading...</td>
            </tr>;
    }
}


export class NifiInstanceDetail extends Component {
    static propTypes = {
        data: PropTypes.object.isRequired
    };

    state = {
        destroyed: false,
        instances_loaded: false,
        instances: []
    };

    refreshInstances() {
        fetch("/api/instance?parent=" + this.props.data.id)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => this.setState({instances: data, instances_loaded: true}));
    }

    componentDidMount() {
        this.refreshInstances();
    }

    handleDestroy = () => {
        console.log("Requesting destruction of nifi instance: " + this.props.data.id);
        fetch("/api/nifi/" + this.props.data.id + "", {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                state: "PENDING_DESTROY"
            })
        }).then(response => {
            if (response.status !== 200) {
                console.log("Failed to request destruction of nifi instance: " + this.props.data.id)
            } else {
                console.log("Requested destruction of nifi instance: " + this.props.data.id);
                perform_cloud_ops();
            }
            return response.json();
        });
        this.setState({destroyed: true});
    };

    render() {
        if (this.state.destroyed) {
            return <Redirect to="/" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <NifiInstancesCrumb/>
                    <CurrentCrumb>{this.props.data.name}</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <h3>{this.props.data.name}</h3>

                        <table className="table is-fullwidth">
                            <tbody>
                            <tr>
                                <td>Image</td>
                                <td>{this.props.data.image}</td>
                            </tr>
                            <tr>
                                <td>URL</td>
                                <td><a
                                    target="_blank"
                                    href={"https://" + this.props.data.hostname + "." + window.nifi_web_config.domain + "/nifi"}>
                                    https://{this.props.data.hostname}.{window.nifi_web_config.domain}/nifi
                                </a>
                                </td>
                            </tr>
                            <tr>
                                <td>Hostname</td>
                                <td>{this.props.data.hostname}</td>
                            </tr>
                            <tr>
                                <td>Namespace</td>
                                <td>{this.props.data.namespace}</td>
                            </tr>
                            {this.props.data.deploy_mongo ?
                                <React.Fragment>
                                    <tr>
                                        <td>Mongo UI</td>
                                        <td>
                                            <a
                                                target="_blank"
                                                href={"https://mongo-" + this.props.data.hostname + "." + window.nifi_web_config.domain}>
                                                {"https://mongo-" + this.props.data.hostname + "." + window.nifi_web_config.domain}
                                            </a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Mongo Host</td>
                                        <td>
                                            mongo
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Mongo Username</td>
                                        <td>
                                            admin
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Mongo Password</td>
                                        <td>
                                            admin
                                        </td>
                                    </tr>
                                </React.Fragment> :
                                <tr>
                                    <td>Mongo</td>
                                    <td>Not deployed</td>
                                </tr>}
                            {this.props.data.deploy_kafka ?
                                <React.Fragment>
                                    <tr>
                                        <td>Kafka Hostname</td>
                                        <td>
                                            kafka
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Kafka Port</td>
                                        <td>
                                            9092
                                        </td>
                                    </tr>
                                </React.Fragment> :
                                <tr>
                                    <td>Kafka</td>
                                    <td>Not deployed</td>
                                </tr>}
                            {this.props.data.deploy_prometheus ?
                                <React.Fragment>
                                    <tr>
                                        <td>Prometheus UI</td>
                                        <td>
                                            <a
                                                target="_blank"
                                                href={"https://prometheus-" + this.props.data.hostname + "." + window.nifi_web_config.domain}>
                                                {"https://prometheus-" + this.props.data.hostname + "." + window.nifi_web_config.domain}
                                            </a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Prometheus Hostname</td>
                                        <td>
                                            prometheus
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Prometheus Port</td>
                                        <td>
                                            9090
                                        </td>
                                    </tr>
                                </React.Fragment> :
                                <tr>
                                    <td>Prometheus</td>
                                    <td>Not deployed</td>
                                </tr>}
                            {this.props.data.deploy_jupyter ?
                                <React.Fragment>
                                    <tr>
                                        <td>Jupyter Notebook Data Science Stack</td>
                                        <td>
                                            <a
                                                target="_blank"
                                                href={"https://jupyter-" + this.props.data.hostname + "." + window.nifi_web_config.domain + "/?token=" + this.props.data.jupyter_token}>
                                                {"https://jupyter-" + this.props.data.hostname + "." + window.nifi_web_config.domain}
                                            </a>
                                        </td>
                                    </tr>
                                </React.Fragment> :
                                <tr>
                                    <td>Jupyter Notebook Data Science Stack</td>
                                    <td>Not deployed</td>
                                </tr>}
                            {this.state.instances_loaded ?
                                this.state.instances.map(instance => <InstanceRow key={instance.id} nifi_instance={this.props.data} instance={instance}/>) :
                                <tr>
                                    <td/>
                                    <td>Loading custom instance types...</td>
                                </tr>}
                            <tr>
                                <td>State</td>
                                <td>{this.props.data.state}</td>
                            </tr>
                            <tr>
                                <td>Cluster</td>
                                <td>
                                    <ClusterMini data={this.props.data.cluster}/>
                                </td>
                            </tr>
                            </tbody>
                        </table>

                        <div className="buttons">
                            <a className="button" onClick={this.handleDestroy}>Destroy Instance</a>
                            <a className="button">Save</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
