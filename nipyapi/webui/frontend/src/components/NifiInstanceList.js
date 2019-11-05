import React, {Component} from "react";
import {Redirect} from "react-router";
import {AdminCrumb, Breadcrumb, CurrentCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {Link} from "react-router-dom";
import {NifiInstanceDetail} from "./NifiInstanceDetail";

export const NifiInstance = ({match}) => (
    <DataProvider endpoint={"/api/nifi/" + match.params.nifiInstanceId}
                  placeholder={<p>Loading...</p>}
                  render={data => <NifiInstanceDetail data={data}/>}/>
);

export class NifiInstanceList extends Component {
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
