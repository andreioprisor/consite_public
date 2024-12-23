module.exports = {
    up: async (queryInterface, Sequelize) => {
        return queryInterface.bulkInsert('products', [
            {
                denumire: 'Teava PVC 1/2 inch',
                doc_id: 1, // Assuming the Document ID from the previous seed
                cantitate: 100,
                pret: 9.99,
                unitate_masura: 'M',
                sup_id: 1, // Assuming the Supplier ID from the previous seed
            },
            // Add more products as needed
        ]);
    },

    down: async (queryInterface, Sequelize) => {
        return queryInterface.bulkDelete('products', null, {});
    },
};
