const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
    class Supplier extends Model {
        static associate(models) {
            // Define associations here
        }
    }

    Supplier.init(
        {
            id: {
                type: DataTypes.INTEGER,
                primaryKey: true,
                autoIncrement: true,
            },
            denumire: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            cod_fiscal: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            reg_com: {
                type: DataTypes.STRING,
                allowNull: true,
            },
            adresa: {
                type: DataTypes.STRING,
                allowNull: true,
            },
            banca: {
                type: DataTypes.STRING,
                allowNull: true,
            },
            cont_bancar: {
                type: DataTypes.STRING,
                allowNull: true,
            },
            persoana_contact: {
                type: DataTypes.STRING,
                allowNull: true,
            },
            telefon: {
                type: DataTypes.STRING,
                allowNull: true,
            },
            email: {
                type: DataTypes.STRING,
                allowNull: true,
            },
        },
        {
            sequelize,
            modelName: 'supplier',
            underscored: true,
            timestamps: false
        },
    );

    return Supplier;
};
