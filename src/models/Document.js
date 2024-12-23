const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
    class Document extends Model {
        static associate(models) {
            // Define associations here
            // Document can have a foreign key relationship with 'furnizor' if needed
            Document.belongsTo(models.supplier, { foreignKey: 'sup_id', targetKey: 'id' });
        }
    }

    Document.init(
        {
            id: {
                type: DataTypes.INTEGER,
                primaryKey: true,
                autoIncrement: true,
            },
            furnizor: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            data_intrare: {
                type: DataTypes.DATE,
                allowNull: false,
            },
            data_scadenta: {
                type: DataTypes.DATE,
                allowNull: true,
            },
            tip: {
                type: DataTypes.INTEGER,
                allowNull: false,
            },
            document_number: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            sup_id: {
                type: DataTypes.INTEGER,
                allowNull: true,
            },
        },
        {
            sequelize,
            modelName: 'document',
            underscored: true,
            timestamps: false, // Disable automatic timestamps if not needed
        },
    );

    return Document;
};
