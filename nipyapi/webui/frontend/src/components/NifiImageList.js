import React, {Component} from "react";
import {Redirect} from "react-router";
import {AdminCrumb, Breadcrumb, CurrentCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {Link} from "react-router-dom";
import {NifiImageDetail} from "./NifiImageDetail";

export const NifiImage = ({match}) => (
    <DataProvider endpoint={"/api/nifi-image/" + match.params.nifiImageId}
                  placeholder={<p>Loading...</p>}
                  render={data => <NifiImageDetail data={data}/>}/>
);

export class NifiImageList extends Component {
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
            return <Redirect to="/create-nifi-image" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <AdminCrumb/>
                    <CurrentCrumb>NiFi Images</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <DataProvider endpoint="/api/nifi-image"
                                      placeholder={<p>Loading...</p>}
                                      render={data => <Table data={data.map(d => {
                                          return {
                                              id: d.id,
                                              "Tag": <Link to={"/nifi-image/" + d.id}>{d.tag}</Link>
                                          }
                                      })}/>} ref="provider"/>
                        <div className="buttons">
                            <a className="button" onClick={this.handleRefresh}>Refresh</a>
                            <a className="button" onClick={this.handleNew}>New Image</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
