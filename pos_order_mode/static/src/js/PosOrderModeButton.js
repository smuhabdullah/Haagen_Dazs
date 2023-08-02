odoo.define('pos_order_mode.PosOrderModeButton', function (require) {
"use strict";
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class OrderModeButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        get currentOrder() {
            return this.env.pos.get_order();
        }
        get getOrderMode() {
            return this.currentOrder ? this.currentOrder.get_order_mode_name() : 'Order Mode';
        }
        async onClick() {
            var order_modes = this.env.pos.db.getOrderModes();
            const selectionList = order_modes.map((orderMode) => ({
                id: orderMode.item,
                label: orderMode.label,
                isSelected: false,
                item: orderMode.item,
            }));
            this.showPopup('SelectionPopup', {
                title: this.env._t('Set Order Mode: '),
                list: selectionList,
            }).then(({ confirmed, payload: selectedorderMode }) => {
                if (confirmed) {
                    this.currentOrder.set_order_mode(this.env.pos.db.get_order_mode_by_id(selectedorderMode))
                }
            });
        }
    }
    OrderModeButton.template = 'OrderModeButton';

    ProductScreen.addControlButton({
        component: OrderModeButton,
        condition: function() {
            // return this.env.pos.config.module_pos_restaurant;
            return true;
        },
    });

    Registries.Component.add(OrderModeButton);

    return OrderModeButton;
});