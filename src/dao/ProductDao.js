const SuperDao = require('./SuperDao');	
const models = require('../models');

const Product = models.product;

class ProductDao extends SuperDao {
	constructor() {
		super(Product);
	}

	// Add specific methods for the Product model here
	
}

module.exports = ProductDao;