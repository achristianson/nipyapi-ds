import React, {Component} from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {BrowserRouter as Router, Link, Redirect, Route} from "react-router-dom";
import {AdminCrumb, Breadcrumb, CurrentCrumb} from "./Breadcrumb";
import {NifiInstanceDetail} from "./NifiInstanceDetail";
import {NifiInstanceNew} from "./NifiInstanceNew";
import {perform_cloud_ops} from "../util/bg_tasks";

const NifiInstance = ({match}) => (
    <DataProvider endpoint={"/api/nifi/" + match.params.nifiInstanceId}
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
                        <DataProvider endpoint="/api/nifi"
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

console.log('requesting config');
fetch("/api/get-config").then(
    response => response.json().then(
        o => {
            console.log('got config');
            window.nifi_web_config = o;
        }
    )
);

perform_cloud_ops();

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render((
    <Router>
        <Route path="/" component={App}>
        </Route>
    </Router>
), wrapper) : null;
