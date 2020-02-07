import React from "react";
import ReactDOM from "react-dom";
import {BrowserRouter as Router, NavLink, Route} from "react-router-dom";
import {NifiInstanceNew} from "./NifiInstanceNew";
import {perform_cloud_ops} from "../util/bg_tasks";
import {NifiInstance, NifiInstanceList} from "./NifiInstanceList";
import {NifiImage, NifiImageList} from "./NifiImageList";
import {NifiImageNew} from "./NifiImageNew";
import {DockerAuthConfig, DockerAuthConfigList} from "./DockerAuthConfigList";
import {DockerAuthConfigNew} from "./DockerAuthConfigNew";
import {DockerAuthConfigDetail} from "./DockerAuthConfigDetail";
import {InstanceType, InstanceTypeList} from "./InstanceTypeList";
import {InstanceTypeNew} from "./InstanceTypeNew";
import {ImageMirror, ImageMirrorList} from "./ImageMirrorList";
import {ImageMirrorNew} from "./ImageMirrorNew";

class App extends React.Component {

    state = {
        config: [],
        loaded: false,
        placeholder: <p>Loading...</p>
    };

    refresh() {
        fetch("/api/get-config")
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => {console.log(data); this.setState({config: data, loaded: true})});
    }

    componentDidMount() {
        this.refresh();
    }
    render() {
        return !this.state.loaded ? <React.Fragment>{this.state.placeholder}</React.Fragment> : (
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
                                    <li><NavLink to="/" exact={true} activeClassName="is-active">NiFi
                                        Instances</NavLink></li>
                                    <li><NavLink to="/nifi-images" activeClassName="is-active">NiFi Images</NavLink>
                                    </li>
                                    <li><a href={"https://registry." + this.state.config.domain + "/nifi-registry"}
                                           target="_blank">Registry</a></li>
                                    {/*<li><a>Kubernetes</a></li>*/}
                                </ul>
                                <p className="menu-label">
                                    Meta
                                </p>
                                <ul className="menu-list">
                                    <li><NavLink to="/instance-types" activeClassName="is-active">Instance Types</NavLink></li>
                                </ul>
                                <p className="menu-label">
                                    Infra
                                </p>
                                <ul className="menu-list">
                                    <li><NavLink to="/mirror-images" activeClassName="is-active">Mirror Images</NavLink></li>
                                </ul>
                                <ul className="menu-list">
                                    <li><NavLink to="/docker-auth-configs" activeClassName="is-active">Docker Auth Configs</NavLink></li>
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
                            <Route path={`/nifi-images`} component={NifiImageList}/>
                            <Route path={`/create-nifi-image`} component={NifiImageNew}/>
                            <Route path={`/nifi-image/:nifiImageId`} component={NifiImage}/>
                            <Route path={`/docker-auth-configs`} component={DockerAuthConfigList}/>
                            <Route path={`/create-docker-auth-config`} component={DockerAuthConfigNew}/>
                            <Route path={`/docker-auth-config/:authConfigId`} component={DockerAuthConfig}/>
                            <Route path={`/instance-types`} component={InstanceTypeList}/>
                            <Route path={`/create-instance-type`} component={InstanceTypeNew}/>
                            <Route path={`/instance-type/:objId`} component={InstanceType}/>
                            <Route path={`/mirror-images`} component={ImageMirrorList}/>
                            <Route path={`/create-mirror-image`} component={ImageMirrorNew}/>
                            <Route path={`/mirror-image/:mirrorId`} component={ImageMirror}/>
                        </div>
                    </div>
                </div>

            </React.Fragment>
        );
    }
}

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
