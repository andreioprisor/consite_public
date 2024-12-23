const httpStatus = require('http-status');

const DocumentDao = require('../dao/DocumentDao');
const SupplierDao = require('../dao/SupplierDao');
const ProductDao = require('../dao/ProductDao');
const logger = require('../config/logger');
const res = require('express/lib/response');
const responseHandler = require('../helper/responseHandler');

class TableService{
	constructor() {
		this.DocumentDao = new DocumentDao();
		this.SupplierDao = new SupplierDao();
		this.ProductDao = new ProductDao();
	}

	getAllRecords = async () => {
		try {
			console.log('Querying all records');
			const records = await this.ProductDao.findAll();
			console.log('Records:', records);
			return records;
		} catch (e) {
			throw e;
		}
	};

	filterRecords = async (filter) => {
		try {
			const records = await this.ProductDao.findByWhere(filter);
			return records;
		} catch (e) {
			throw e;
		}
	};

	updateProduct = async (updatedData, id) => {
		try {
			const message = 'Successfully updated product';
			const newRecord = await this.ProductDao.updateById(updatedData, id);
			// if there is no error thrown, return a message with success status
			return newRecord;
		} catch (e) {
			console.log(e);
			throw e;
		}
	};

	createProducts = async (docBody, supplierBody, productsBody) => {
		try {
			console.log('Creating products with data:', docBody, supplierBody, productsBody);
			let document = await this.DocumentDao.findOneByWhere({
				document_number: docBody.document_number,
				furnizor: docBody.furnizor
			});
	
			if (document) {
				// If document exists, use the existing document ID
				console.log('Document already exists with ID:', document.id);
				return responseHandler.returnError(httpStatus.BAD_REQUEST, 'Document already exists');
			} else {
				// If document does not exist, create it and use the new ID
				document = await this.DocumentDao.create(docBody);
			}
	
			let supplier = await this.SupplierDao.findOneByWhere({
				denumire: supplierBody.denumire
			});
	
			if (!supplier) {
				console.log('Supplier does not exist, creating new');
				supplier = await this.SupplierDao.create(supplierBody);
			}
	
			// Map through productsBody to attach correct `doc_id` and `sup_id`
			const productsWithIds = productsBody.map(product => ({
				...product,
				doc_id: document.id,  // Ensure this is the document ID
				sup_id: supplier.id   // Ensure this is the supplier ID
			}));
	
			// Bulk create products with proper foreign keys set
			const products = await this.ProductDao.bulkCreate(productsWithIds);
	
			return responseHandler.returnSuccess(httpStatus.CREATED, 'Successfully added products', products);
		} catch (e) {
			console.error('Error in createProducts:', e);
			return responseHandler.returnError(httpStatus.BAD_REQUEST, 'Something went wrong!');
		}
	};
	

}

module.exports = TableService;