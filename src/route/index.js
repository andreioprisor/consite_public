const express = require('express');
const authRoute = require('./authRoute');
const santierRoute = require('./santierRoute');
const router = express.Router();

const defaultRoutes = [
    {
        path: '/auth',
        route: authRoute,
    },
    {
        path: '/tables',
        route: santierRoute,
    },
];

defaultRoutes.forEach((route) => {
    router.use(route.path, route.route);
});

module.exports = router;
