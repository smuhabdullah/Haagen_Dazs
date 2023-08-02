odoo.define('pos_payment_disc.PaymentScreen', function(require) {
'use strict';

    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');


    const PaymentScreenDisc = (PaymentScreen) =>
       class extends PaymentScreen {
            /**
             * @override
             */
            deletePaymentLine(event) {
                const { cid } = event.detail;
                const line = this.paymentLines.find((line) => line.cid === cid);
                const paymentMethod = line.payment_method
                if (paymentMethod.apply_discount){
                    const discount_product_id = paymentMethod.discount_product_id[0]
                    const res = super.deletePaymentLine(event);
                    const order = this.env.pos.get_order();
                    this.remove_discount(discount_product_id)
                    order.trigger('change', order);
                    this.render();    
                }
                else{
                    const res = super.deletePaymentLine(event);
                }
                
            }
            addNewPaymentLine({ detail: paymentMethod }) {
                if (paymentMethod.apply_discount){
                    const order = this.env.pos.get_order();
                    const discount_product_id = paymentMethod.discount_product_id[0]
                    
                    if (paymentMethod.total_discount && discount_product_id) {
                        this.apply_discount(discount_product_id,paymentMethod.total_discount)
                        order.trigger('change', order);
                        this.render();
                        }
                    const res = super.addNewPaymentLine(...arguments);
                }
                else{
                    const res = super.addNewPaymentLine(...arguments);
                }
            }
            async remove_discount(discount_product_id) {
                const order = this.env.pos.get_order();
                var lines    = order.get_orderlines();
                var product  = this.env.pos.db.get_product_by_id(discount_product_id);
                if (product === undefined) {
                    await this.showPopup('ErrorPopup', {
                        title : this.env._t("No discount product found"),
                        body  : this.env._t("The discount product seems misconfigured on selected payment method. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
                    });
                    return;
                }
    
                // Remove existing discounts
                for (const line of lines) {
                    if (line.get_product() === product) {
                        order.remove_orderline(line);
                    }
                }
            }
            async apply_discount(discount_product_id,pc) {
                var order    = this.env.pos.get_order();
                var lines    = order.get_orderlines();
                var product  = this.env.pos.db.get_product_by_id(discount_product_id);
                if (product === undefined) {
                    await this.showPopup('ErrorPopup', {
                        title : this.env._t("No discount product found"),
                        body  : this.env._t("The discount product seems misconfigured on selected payment method. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
                    });
                    return;
                }
    
                // Remove existing discounts
                for (const line of lines) {
                    if (line.get_product() === product) {
                        order.remove_orderline(line);
                    }
                }
    
                // Add discount
                // We add the price as manually set to avoid recomputation when changing customer.
                var base_to_discount = order.get_total_without_tax();
                if (product.taxes_id.length){
                    var first_tax = this.env.pos.taxes_by_id[product.taxes_id[0]];
                    if (first_tax.price_include) {
                        base_to_discount = order.get_total_with_tax();
                    }
                }
                var discount = - pc / 100.0 * base_to_discount;
    
                if( discount < 0 ){
                    order.add_product(product, {
                        price: discount,
                        lst_price: discount,
                        extras: {
                            price_manually_set: true,
                        },
                    });
                }
            }

        };
    Registries.Component.extend(PaymentScreen, PaymentScreenDisc);
    return PaymentScreenDisc;

});

