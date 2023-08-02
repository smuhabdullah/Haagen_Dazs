odoo.define('pos_payment_disc.models', function(require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields("pos.payment.method", ["apply_discount","total_discount","discount_product_id"]);
});