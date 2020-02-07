import React, {Component} from "react";
import {Redirect} from "react-router";
import {AdminCrumb, Breadcrumb, CurrentCrumb} from "./Breadcrumb";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {Link} from "react-router-dom";
import {ImageMirrorDetail} from "./ImageMirrorDetail";

export const ImageMirror = ({match}) => (
    <DataProvider endpoint={"/api/image-mirror/" + match.params.mirrorId}
                  placeholder={<p>Loading...</p>}
                  render={data => <ImageMirrorDetail data={data}/>}/>
);

export class ImageMirrorList extends Component {
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
            return <Redirect to="/create-mirror-image" push={true}/>;
        }

        return (
            <React.Fragment>
                <Breadcrumb>
                    <AdminCrumb/>
                    <CurrentCrumb>Mirror Images</CurrentCrumb>
                </Breadcrumb>
                <section className="">
                    <div className="content">
                        <DataProvider endpoint="/api/image-mirror"
                                      placeholder={<p>Loading...</p>}
                                      render={data => <Table data={data.map(d => {
                                          return {
                                              id: d.id,
                                              "From Image": <Link to={"/mirror-image/" + d.id}>{d.from_image}</Link>,
                                              "To Image": d.to_image
                                          }
                                      })}/>} ref="provider"/>
                        <div className="buttons">
                            <a className="button" onClick={this.handleRefresh}>Refresh</a>
                            <a className="button" onClick={this.handleNew}>New Mirror Image</a>
                        </div>
                    </div>
                </section>
            </React.Fragment>
        );
    }
}
