odoo.define('point_of_sale.OpeningStockDetailsPopup', function(require) {
    'use strict';

    const { useState } = owl.hooks;
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class OpeningStockDetailsPopup extends PosComponent {
        constructor() {
            super(...arguments);
            this.product_lines = []
            this.state = useState({
                total: 0,
            });
        }
        async fetchProductDetails() {
            var session_products = []
            var location = this.env.pos.config.default_location_src_id
            var domain = [['quantity', '>', 0],['show_in_pos_session','=',true]]
            if (location){
                domain.push('|', ['location_id', '=', false], ['location_id', 'child_of', [location[0]]])
            }
            const quants = await this.rpc({
                model: 'stock.quant',
                method: 'search_read',
                orderBy: [{name: 'product_id', asc: true}],
                domain: domain,
                fields: ['product_id', 'available_quantity'],
            });
            quants.forEach((quant) => { 
                    session_products.push({
                        product: quant['product_id'][1],
                        quantity: quant['available_quantity']
                    }) 
                })
            return session_products;
        }
        isClosed() {
            return this.el.classList.contains('invisible')
        }
        openPopup() {
            this.el.classList.remove('invisible');
        }
        _closePopup() {
            this.el.classList.add('invisible');
        }
        discard() {
            this._closePopup();
        }
    }

    OpeningStockDetailsPopup.template = 'OpeningStockDetailsPopup';
    Registries.Component.add(OpeningStockDetailsPopup);

    return OpeningStockDetailsPopup;

});
