odoo.define('pos_order_mode.DB', function (require) {
	"use strict";

var utils = require('web.utils');
var PosDB = require("point_of_sale.DB");
PosDB.include({
    init: function(options){
        this._super(options);
        this.order_mode_sorted = [];
        this.order_mode_by_id = {};
        this.order_mode_search_string = "";
        this.order_mode_write_date = null;
        
    },
    _order_mode_search_string: function(order_mode){
        var str =  order_mode.name || '';
        if(order_mode.address){
            str += '|' + order_mode.address;
        }
        if(order_mode.phone){
            str += '|' + order_mode.phone.split(' ').join('');
        }
        if(order_mode.mobile){
            str += '|' + order_mode.mobile.split(' ').join('');
        }
        if(order_mode.email){
            str += '|' + order_mode.email;
        }
        str = '' + order_mode.id + ':' + str.replace(':','') + '\n';
        return str;
    },
    add_order_modes: function(order_modes){
        var updated_count = 0;
        var new_write_date = '';
        var order_mode;
        for(var i = 0, len = order_modes.length; i < len; i++){
            order_mode = order_modes[i];

            var local_order_mode_date = (this.order_mode_write_date || '').replace(/^(\d{4}-\d{2}-\d{2}) ((\d{2}:?){3})$/, '$1T$2Z');
            var dist_order_mode_date = (order_mode.write_date || '').replace(/^(\d{4}-\d{2}-\d{2}) ((\d{2}:?){3})$/, '$1T$2Z');
            if (    this.order_mode_write_date &&
                    this.order_mode_by_id[order_mode.id] &&
                    new Date(local_order_mode_date).getTime() + 1000 >=
                    new Date(dist_order_mode_date).getTime() ) {
                // FIXME: The write_date is stored with milisec precision in the database
                // but the dates we get back are only precise to the second. This means when
                // you read order_modes modified strictly after time X, you get back order_modes that were
                // modified X - 1 sec ago. 
                continue;
            } else if ( new_write_date < order_mode.write_date ) { 
                new_write_date  = order_mode.write_date;
            }
            if (!this.order_mode_by_id[order_mode.id]) {
                this.order_mode_sorted.push(order_mode.id);
            }
            this.order_mode_by_id[order_mode.id] = order_mode;

            updated_count += 1;
        }

        this.order_mode_write_date = new_write_date || this.order_mode_write_date;

        if (updated_count) {
            // If there were updates, we need to completely 

            this.order_mode_search_string = "";

            for (var id in this.order_mode_by_id) {
                order_mode = this.order_mode_by_id[id];
                // order_mode.address = (order_mode.street ? order_mode.street + ', ': '') +
                //                   (order_mode.zip ? order_mode.zip + ', ': '') +
                //                   (order_mode.city ? order_mode.city + ', ': '') +
                //                   (order_mode.state_id ? order_mode.state_id[1] + ', ': '') +
                //                   (order_mode.country_id ? order_mode.country_id[1]: '');
                this.order_mode_search_string += this._order_mode_search_string(order_mode);
            }

            this.order_mode_search_string = utils.unaccent(this.order_mode_search_string);
        }
        return updated_count;
    },
    get_order_mode_write_date: function(){
        return this.order_mode_write_date || "1970-01-01 00:00:00";
    },
    get_order_mode_by_id: function(id){
        return this.order_mode_by_id[id];
    },
    get_order_modes_sorted: function(max_count){
        max_count = max_count ? Math.min(this.order_mode_sorted.length, max_count) : this.order_mode_sorted.length;
        var order_modes = [];
        for (var i = 0; i < max_count; i++) {
            order_modes.push(this.order_mode_by_id[this.order_mode_sorted[i]]);
        }
        return order_modes;
    },
    getOrderModes: function () {
        var pos_order_modes = [];

        $.each(this.get_order_modes_sorted(100), function (i, order_mode) {
            // if (order_mode.pos_mercury_config_id) {
            pos_order_modes.push({label: order_mode.name, item: order_mode.id});
            // }
        });

        return pos_order_modes;
    },
    // search_steward: function(query){
    //     try {
    //         query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,'.');
    //         query = query.replace(/ /g,'.+');
    //         var re = RegExp("([0-9]+):.*?"+utils.unaccent(query),"gi");
    //     }catch(e){
    //         return [];
    //     }
    //     var results = [];
    //     for(var i = 0; i < this.limit; i++){
    //         var r = re.exec(this.steward_search_string);
    //         if(r){
    //             var id = Number(r[1]);
    //             results.push(this.get_steward_by_id(id));
    //         }else{
    //             break;
    //         }
    //     }
    //     return results;
    // },
});
});