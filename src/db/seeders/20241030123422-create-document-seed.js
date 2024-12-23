module.exports = {
    up: async (queryInterface, Sequelize) => {
        return queryInterface.bulkInsert('documents', [
            {
                furnizor: 'ABC Supplies',
                data_intrare: new Date(),
                data_scadenta: new Date(new Date().setDate(new Date().getDate() + 30)), // 30 days later
                tip: 1,
                document_number: 'DOC001',
                sup_id: 1, // Assuming the Supplier ID from the previous seed
            },
            // Add more documents as needed
        ]);
    },

    down: async (queryInterface, Sequelize) => {
        return queryInterface.bulkDelete('documents', null, {});
    },
};
