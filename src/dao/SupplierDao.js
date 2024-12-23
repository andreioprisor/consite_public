const SuperDao = require('./SuperDao');
const models = require('../models');

const Supplier = models.supplier;

class SupplierDao extends SuperDao {
    constructor() {
        super(Supplier);
    }

    // Method to check if a supplier exists by its name
    isSupplierExists = async (nume) => {
        console.log('Checking if supplier exists:', nume);
        try {
            const condition = {
                denumire: nume // Match this with your database column name (likely 'denumire')
            };

            const supplier = await this.findOneByWhere(condition);

            return supplier ? supplier.id : -1;
        } catch (error) {
            console.error('Error checking if supplier exists:', error);
            throw error;
        }
    }
}

module.exports = SupplierDao;