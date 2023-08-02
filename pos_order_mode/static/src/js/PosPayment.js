odoo.define("pos_order_mode.pos_choosing_mode", function (require) {
    "use strict";
    /* global Sha1*/
    const Registries = require("point_of_sale.Registries");
    const ProductScreen = require("point_of_sale.ProductScreen");

    const PosProductScreen = (_ProductScreen) =>
        class extends _ProductScreen {
            constructor() {
                super(...arguments);
            }

            async _onClickPay() {
                const currentOrder = this.env.pos.get_order()
                const currentOrderMode = currentOrder.get_order_mode();
                // console.log(currentOrderMode)
                if (currentOrderMode == null){
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
                            currentOrder.set_order_mode(this.env.pos.db.get_order_mode_by_id(selectedorderMode))
                            this.showScreen("PaymentScreen");
                        }
                    });
                }
                else{
                    this.showScreen("PaymentScreen");
                }
            }
      };

    Registries.Component.extend(ProductScreen, PosProductScreen);

    return ProductScreen;
});