module.exports = {
    up: async (queryInterface, Sequelize) => {
        await queryInterface.createTable('documents', {
            id: {
                allowNull: false,
                autoIncrement: true,
                primaryKey: true,
                type: Sequelize.INTEGER,
            },
            furnizor: {
                type: Sequelize.STRING,
                allowNull: false,
            },
            data_intrare: {
                type: Sequelize.DATE,
                allowNull: false,
            },
            data_scadenta: {
                type: Sequelize.DATE,
                allowNull: true,
            },
            tip: {
                type: Sequelize.INTEGER,
                allowNull: false,
            },
            document_number: {
                type: Sequelize.STRING,
                allowNull: false,
            },
            sup_id: {
                type: Sequelize.INTEGER,
                allowNull: true,
                references: {
                    model: 'suppliers', // Name of the table being referenced
                    key: 'id',          // Primary key in the suppliers table
                },
            },
        });
    },

    down: async (queryInterface, Sequelize) => {
        await queryInterface.dropTable('documents');
    },
};
