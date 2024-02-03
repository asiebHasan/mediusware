import React from 'react'

function EditProduct(props) {

    const product = props.product
    console.log(product.title);
    console.log(props.product.sku);
    console.log(props.product.description);
    return (
        <div>
            <section>
                EditProduct
                {product}
            </section>
        </div>
    )
}

export default EditProduct