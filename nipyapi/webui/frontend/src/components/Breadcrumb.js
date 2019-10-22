import React from "react";
import {Link} from "react-router-dom";

export const Breadcrumb = props => (
    <nav className="breadcrumb" aria-label="breadcrumbs">
        <ul>
            {props.children}
        </ul>
    </nav>
);

export const CurrentCrumb = props => (
    <li className="is-active"><a href="#" aria-current="page">{props.children}</a></li>
);

export const AdminCrumb = () => (
    <li><Link to="/">Admin</Link></li>
);

export const NifiInstancesCrumb = () => (
    <React.Fragment>
        <AdminCrumb/>
        <li><Link to="/">NiFi Instances</Link></li>
    </React.Fragment>
);
