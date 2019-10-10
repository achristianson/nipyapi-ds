import React, {Component} from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {BrowserRouter as Router, Route, Link, Redirect} from "react-router-dom";
import PropTypes from "prop-types";
import key from "weak-key";

const Breadcrumb = props => (
    <nav className="breadcrumb" aria-label="breadcrumbs">
        <ul>
            {props.children}
        </ul>
    </nav>
);

const CurrentCrumb = props => (
    <li className="is-active"><a href="#" aria-current="page">{props.children}</a></li>
);

const AdminCrumb = () => (
    <li><Link to="/">Admin</Link></li>
);

const NifiInstancesCrumb = () => (
    <React.Fragment>
        <AdminCrumb/>
        <li><Link to="/">NiFi Instances</Link></li>
    </React.Fragment>
);

class NifiInstanceNew extends Component {
    state = {
        name: "",
        creating: false,
        submitted: false,
        cluster: 0
    };

    handleSubmit = e => {
        e.preventDefault();
        this.setState({creating: true});
        const inst = {
            name: this.state.name,
            cluster: parseInt(this.state.cluster)
        };
        const conf = {
            method: "POST",
            body: JSON.stringify(inst),
            headers: new Headers({"Content-Type": "application/json"})
        };
        fetch("/api/nifi/", conf).then(response => this.setState({submitted: true}));

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
                            <label className="label">K8s Cluster</label>
                            <div className="control">
                                <select name="cluster" value={this.state.cluster} onChange={this.handleChange}>
                                    <option key=""/>
                                    <DataProvider endpoint={"/api/k8s-cluster/"}
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

class NifiInstanceDetail extends Component {
    static propTypes = {
        data: PropTypes.object.isRequired
    };

    state = {
        destroyed: false
    };

    handleDestroy = () => {
        console.log("Requesting destruction of nifi instance: " + this.props.data.id);
        fetch("/api/nifi/" + this.props.data.id + "/", {
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
                console.log("Requested destruction of nifi instance: " + this.props.data.id)
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
                        {/*<DataProvider endpoint="api/nifi/"*/}
                        {/*              render={data => <Table data={data.map(d => {*/}
                        {/*                  return {*/}
                        {/*                      id: d.id,*/}
                        {/*                      "Instance": <Link to={"/nifi/" + d.id}>{d.name}</Link>*/}
                        {/*                  }*/}
                        {/*              })}/>}/>*/}
                        <h3>{this.props.data.name}</h3>

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

const NifiInstance = ({match}) => (
    <DataProvider endpoint={"/api/nifi/" + match.params.nifiInstanceId + "/"}
                  placeholder={<p>Loading...</p>}
                  render={data => <NifiInstanceDetail data={data}/>}/>
);

class NifiInstanceList extends Component {
    state = {
        adding: false
    };

    handleRefresh = () => {
        this.refs.provider.refresh();
    };

    handleNew = () => {
        this.setState({
            adding: true
        })
    };

    render() {
        if (this.state.adding) {
            return <Redirect to="/create_nifi" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <AdminCrumb/>
                    <CurrentCrumb>NiFi Instances</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <DataProvider endpoint="/api/nifi/"
                                      placeholder={<p>Loading...</p>}
                                      render={data => <Table data={data.map(d => {
                                          return {
                                              id: d.id,
                                              "Instance": <Link to={"/nifi/" + d.id}>{d.name}</Link>,
                                              "State": d.state
                                          }
                                      })}/>} ref="provider"/>
                        <div className="buttons">
                            <a className="button" onClick={this.handleRefresh}>Refresh</a>
                            <a className="button" onClick={this.handleNew}>New Instance</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}

const App = () => (
    <React.Fragment>
        <nav className="navbar is-white">
            <div className="container">
                <div className="navbar-brand">
                    <a className="navbar-item brand-text" href="../">
                        Admin
                    </a>
                </div>
                {/*<div id="navMenu" className="navbar-menu">*/}
                {/*    <div className="navbar-start">*/}
                {/*        <a className="navbar-item" href="admin.html">*/}
                {/*            Home*/}
                {/*        </a>*/}
                {/*        <a className="navbar-item" href="admin.html">*/}
                {/*            Orders*/}
                {/*        </a>*/}
                {/*        <a className="navbar-item" href="admin.html">*/}
                {/*            Payments*/}
                {/*        </a>*/}
                {/*        <a className="navbar-item" href="admin.html">*/}
                {/*            Exceptions*/}
                {/*        </a>*/}
                {/*    </div>*/}
                {/*</div>*/}
            </div>
        </nav>

        <div className="container">
            <div className="columns">
                <div className="column is-3 ">
                    <aside className="menu">
                        <p className="menu-label">
                            General
                        </p>
                        <ul className="menu-list">
                            <li><a className="is-active">NiFi Instances</a></li>
                            <li><a>Kubernetes</a></li>
                        </ul>
                        <p className="menu-label">
                            Debug
                        </p>
                        <ul className="menu-list">
                            <li><a>Events</a></li>
                        </ul>
                    </aside>
                </div>
                <div className="column is-9">
                    <Route exact path="/" component={NifiInstanceList}/>
                    <Route path={`/create_nifi`} component={NifiInstanceNew}/>
                    <Route path={`/nifi/:nifiInstanceId`} component={NifiInstance}/>
                </div>
            </div>
        </div>

    </React.Fragment>
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render((
    <Router>
        <Route path="/" component={App}>
        </Route>
    </Router>
), wrapper) : null;
