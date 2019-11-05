import React from "react";
import ReactDOM from "react-dom";
import {BrowserRouter as Router, NavLink, Route} from "react-router-dom";
import {NifiInstanceNew} from "./NifiInstanceNew";
import {perform_cloud_ops} from "../util/bg_tasks";
import {NifiInstance, NifiInstanceList} from "./NifiInstanceList";
import {NifiImage, NifiImageList} from "./NifiImageList";
import {NifiImageNew} from "./NifiImageNew";

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
                            <li><NavLink to="/" exact={true} activeClassName="is-active">NiFi Instances</NavLink></li>
                            <li><NavLink to="/nifi-images" activeClassName="is-active">NiFi Images</NavLink></li>
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
                    <Route path={`/nifi-images`} component={NifiImageList}/>
                    <Route path={`/create-nifi-image`} component={NifiImageNew}/>
                    <Route path={`/nifi-image/:nifiImageId`} component={NifiImage}/>
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
