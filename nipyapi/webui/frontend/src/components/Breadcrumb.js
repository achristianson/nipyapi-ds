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

export const NifiImagesCrumb = () => (
    <React.Fragment>
        <AdminCrumb/>
        <li><Link to="/nifi-images">NiFi Images</Link></li>
    </React.Fragment>
);

export const ImageMirrorsCrumb = () => (
    <React.Fragment>
        <AdminCrumb/>
        <li><Link to="/mirror-images">Mirror Images</Link></li>
    </React.Fragment>
);

export const DockerAuthConfigsCrumb = () => (
    <React.Fragment>
        <AdminCrumb/>
        <li><Link to="/docker-auth-configs">Docker Auth Configs</Link></li>
    </React.Fragment>
);

export const InstanceTypesCrumb = () => (
    <React.Fragment>
        <AdminCrumb/>
        <li><Link to="/instance-types">Instance Types</Link></li>
    </React.Fragment>
);
