odoo.define('pos_order_mode.PosOrderModeLoad', function (require) {
	"use strict";
	
    var models = require('point_of_sale.models');

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        
        get_order_mode: function(){
            if (this.order_mode) {
                return this.order_mode.id;
            }
            else {
                return null
            }
        },
        set_order_mode: function(order_mode){
            this.order_mode_id = order_mode.id;
            this.order_mode = order_mode;
            this.set('order_mode',order_mode);
        },
        get_order_mode_name: function(){
            var order_mode = this.get('order_mode');
            return order_mode ? order_mode.name : "Order Mode";
        },
        export_as_JSON: function() {
            var data = _super_order.export_as_JSON.apply(this, arguments);
            data.order_mode_id = this.get_order_mode();
            data.order_mode = this.order_mode;
            return data;
        },
        init_from_JSON: function(json) {
            this.order_mode_id = json.order_mode_id;
            this.order_mode = json.order_mode;
            _super_order.init_from_JSON.call(this, json);
        },
    });

    models.load_models({
        model: 'pos.modes',
        fields: ['id','name'],
        domain: null,
        loaded: function (self, order_modes) {
            self.order_modes = order_modes;
            self.order_modes_by_id = {};
            for (var i = 0; i < order_modes.length; i++) {
                self.order_modes_by_id[order_modes[i].id] = order_modes[i];
            }
            self.db.add_order_modes(order_modes);
            }
	});
    // models.PosModel = pos_model.PosModel.extend({
        
    // });
});
