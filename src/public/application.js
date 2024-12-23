// Define the base URL depending on the environment
// var baseURL = window.location.hostname === 'localhost' ? 'http://localhost:3000' : 'https://your-production-domain.com';
var baseURL = 'http://localhost:5000';

document.getElementById('fetchAll').addEventListener('click', function() {
    axios.get(baseURL + '/api/products')
        .then(response => {
            document.getElementById('fetchAllResults').innerHTML = JSON.stringify(response.data, null, 2);
        })
        .catch(error => console.error('Error fetching products:', error));
});

document.getElementById('filterForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const filter = document.getElementById('filterField').value;
    axios.post(baseURL + '/api/products/filter', { filter: JSON.parse(filter) })
        .then(response => {
            document.getElementById('filterResults').innerHTML = JSON.stringify(response.data, null, 2);
        })
        .catch(error => console.error('Error filtering products:', error));
});

document.getElementById('updateForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const id = document.getElementById('updateId').value;
    const updatedData = document.getElementById('updateData').value;
    axios.put(baseURL + `/api/products/update/${id}`, JSON.parse(updatedData))
        .then(response => {
            alert('Product updated successfully!');
        })
        .catch(error => console.error('Error updating product:', error));
});

document.getElementById('addDocsForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const docBody = JSON.parse(document.getElementById('docData').value);
    const supplierBody = JSON.parse(document.getElementById('supplierData').value);
    const productsBody = JSON.parse(document.getElementById('productsData').value);
    axios.post(baseURL + '/api/docs/add', { docBody, supplierBody, productsBody })
        .then(response => {
            alert('Document and products added successfully!');
        })
        .catch(error => console.error('Error adding document:', error));
});
