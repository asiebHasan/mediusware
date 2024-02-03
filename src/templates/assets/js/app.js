import React from "react";
import ReactDOM from "react-dom";
import CreateProduct from "./components/CreateProduct";
import EditProduct from "./components/EditProduct";

// require('./bootstrap');
// require('./sb-admin');

const propsContainer = document.getElementById("product");
const props = Object.assign({}, propsContainer.dataset);



const isEditMode = document.getElementById('root').getAttribute('data-edit-mode')

console.log(isEditMode)

ReactDOM.render(
    <React.StrictMode>
        {isEditMode ? <EditProduct {...props} /> : <CreateProduct {...props} />}
    </React.StrictMode>,
    document.getElementById('root')
);
