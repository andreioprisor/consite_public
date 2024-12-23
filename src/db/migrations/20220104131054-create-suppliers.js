module.exports = {
    up: async (queryInterface, Sequelize) => {
        await queryInterface.createTable('suppliers', {
            id: {
                allowNull: false,
                autoIncrement: true,
                primaryKey: true,
                type: Sequelize.INTEGER,
            },
            denumire: {
                type: Sequelize.STRING,
                allowNull: false,
            },
            cod_fiscal: {
                type: Sequelize.STRING,
                allowNull: false,
            },
            reg_com: {
                type: Sequelize.STRING,
                allowNull: true,
            },
            adresa: {
                type: Sequelize.STRING,
                allowNull: true,
            },
            banca: {
                type: Sequelize.STRING,
                allowNull: true,
            },
            cont_bancar: {
                type: Sequelize.STRING,
                allowNull: true,
            },
            persoana_contact: {
                type: Sequelize.STRING,
                allowNull: true,
            },
            telefon: {
                type: Sequelize.STRING,
                allowNull: true,
            },
            email: {
                type: Sequelize.STRING,
                allowNull: true,
            },
        });
    },

    down: async (queryInterface, Sequelize) => {
        await queryInterface.dropTable('suppliers');
    },
};
