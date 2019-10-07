import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";

const Table = ({data}) =>
    !data.length ? (
        <p>Nothing to show</p>
    ) : (
        <table className="table is-striped">
            <thead>
            <tr>
                {Object.entries(data[0]).map(el => el[0] !== "id" ? <th key={key(el)}>{el[0]}</th> : null)}
            </tr>
            </thead>
            <tbody>
            {data.map(el => (
                <tr key={el.id}>
                    {Object.entries(el).map(el => el[0] !== "id" ? <td key={key(el)}>{el[1]}</td> : null)}
                </tr>
            ))}
            </tbody>
        </table>
    );

Table.propTypes = {
    data: PropTypes.array.isRequired
};

export default Table;
