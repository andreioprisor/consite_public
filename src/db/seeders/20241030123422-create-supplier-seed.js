const bcrypt = require('bcryptjs');

module.exports = {
    up: async (queryInterface, Sequelize) => {
        return queryInterface.bulkInsert('suppliers', [
            {
                denumire: 'ABC Supplies',
                cod_fiscal: 'RO123456789',
                reg_com: 'J12/3456/2020',
                adresa: '1234 Main St, City, Country',
                banca: 'BCR',
                cont_bancar: 'RO49AAAA1B31007593840000',
                persoana_contact: 'John Doe',
                telefon: '1234567890',
                email: 'dani.mocanu@gmail.com'
            },
            // Add more suppliers as needed
        ]);
    },

    down: async (queryInterface, Sequelize) => {
        return queryInterface.bulkDelete('suppliers', null, {});
    },
};
