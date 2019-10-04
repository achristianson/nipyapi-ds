import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";

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
                            <li><a className="is-active">Nifi Instances</a></li>
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
                    <nav className="breadcrumb" aria-label="breadcrumbs">
                        <ul>
                            <li><a href="../">Admin</a></li>
                            {/*<li><a href="../">Templates</a></li>*/}
                            {/*<li><a href="../">Examples</a></li>*/}
                            <li className="is-active"><a href="#" aria-current="page">NiFi Instances</a></li>
                        </ul>
                    </nav>
                    <section className="">
                        <DataProvider endpoint="api/nifi/"
                                      render={data => <Table data={data}/>}/>
                    </section>
                </div>
            </div>
        </div>

    </React.Fragment>
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App/>, wrapper) : null;
