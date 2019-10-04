import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";

const Table = ({data}) =>
    !data.length ? (
        <p>Nothing to show</p>
    ) : (
        <div className="content">
            <div className="buttons">
                <a className="button">Refresh</a>
                <a className="button">Create Instance</a>
            </div>
            <table className="table is-striped">
                <thead>
                <tr>
                    {Object.entries(data[0]).map(el => <th key={key(el)}>{el[0]}</th>)}
                </tr>
                </thead>
                <tbody>
                {console.log("hi")}
                {data.map(el => (
                    <tr key={el.id}>
                        {Object.entries(el).map(el => <td key={key(el)}>{el[1]}</td>)}
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );

Table.propTypes = {
    data: PropTypes.array.isRequired
};

export default Table;
