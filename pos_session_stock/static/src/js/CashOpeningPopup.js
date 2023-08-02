odoo.define('pos_session_stock.CashOpeningPopup', function(require) {
    'use strict';

    const CashOpeningPopup = require('point_of_sale.CashOpeningPopup');
    const Registries = require('point_of_sale.Registries');
    const { useRef } = owl.hooks;
    
    const CashOpeningStockPopup = CashOpeningPopup =>
        class extends CashOpeningPopup {
            constructor() {
                super(...arguments);
                // this.state = useState({
                //     notes: "",
                //     openingCash: this.env.pos.bank_statement.balance_start || 0,
                // });
                this.openingStockDetailsRef = useRef('openingStockDetails');
            }
            async openStockDetailsPopup() {
                if (this.openingStockDetailsRef.comp.isClosed()){
                    this.openingStockDetailsRef.comp.openPopup();
                    // this.state.openingCash = 0;
                    // this.state.notes = "";
                    // if (this.manualInputCashCount) {
                    //     this.openingStockDetailsRef.comp.reset();
                    // }
                }
            }
        };

    Registries.Component.extend(CashOpeningPopup, CashOpeningStockPopup);

    return CashOpeningStockPopup;
});
