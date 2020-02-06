import React, {Component} from "react";
import {Redirect} from "react-router";
import {AdminCrumb, Breadcrumb, CurrentCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {Link} from "react-router-dom";
import {NifiImageDetail} from "./NifiImageDetail";
import {DockerAuthConfigDetail} from "./DockerAuthConfigDetail";

export const DockerAuthConfig = ({match}) => (
    <DataProvider endpoint={"/api/docker-registry-auth/" + match.params.authConfigId}
                  placeholder={<p>Loading...</p>}
                  render={data => <DockerAuthConfigDetail data={data}/>}/>
);

export class DockerAuthConfigList extends Component {
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
            return <Redirect to="/create-docker-auth-config" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <AdminCrumb/>
                    <CurrentCrumb>Docker Auth Configs</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <DataProvider endpoint="/api/docker-registry-auth"
                                      placeholder={<p>Loading...</p>}
                                      render={data => <Table data={data.map(d => {
                                          return {
                                              id: d.id,
                                              "Name": <Link to={"/docker-auth-config/" + d.id}>{d.name}</Link>
                                          }
                                      })}/>} ref="provider"/>
                        <div className="buttons">
                            <a className="button" onClick={this.handleRefresh}>Refresh</a>
                            <a className="button" onClick={this.handleNew}>New Config</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
