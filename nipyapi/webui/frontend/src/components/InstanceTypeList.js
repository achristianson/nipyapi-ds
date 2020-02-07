import React, {Component} from "react";
import {Redirect} from "react-router";
import {AdminCrumb, Breadcrumb, CurrentCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {Link} from "react-router-dom";
import {NifiImageDetail} from "./NifiImageDetail";
import {DockerAuthConfigDetail} from "./DockerAuthConfigDetail";

export const InstanceType = ({match}) => (
    <DataProvider endpoint={"/api/instance-type/" + match.params.objId}
                  placeholder={<p>Loading...</p>}
                  render={data => <InstanceTypeDetail data={data}/>}/>
);

export class InstanceTypeList extends Component {
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
            return <Redirect to="/create-instance-type" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <AdminCrumb/>
                    <CurrentCrumb>Instance Types</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <DataProvider endpoint="/api/instance-type"
                                      placeholder={<p>Loading...</p>}
                                      render={data => <Table data={data.map(d => {
                                          return {
                                              id: d.id,
                                              "Name": <Link to={"/instance-type/" + d.id}>{d.name}</Link>
                                          }
                                      })}/>} ref="provider"/>
                        <div className="buttons">
                            <a className="button" onClick={this.handleRefresh}>Refresh</a>
                            <a className="button" onClick={this.handleNew}>New Instance Type</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
