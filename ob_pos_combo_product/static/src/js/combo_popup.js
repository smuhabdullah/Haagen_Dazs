odoo.define('ob_pos_combo_product.combo_popup', function(require) {
    'use strict';

    const Popup = require('point_of_sale.ConfirmPopup');
    const Registries = require('point_of_sale.Registries');

    class ComboPopup extends Popup {
        constructor() {
            super(...arguments);
        }
        confirm() {
            this.props.resolve({
                confirmed: true,
                payload: { props: this.props},
            });
            this.trigger('close-popup');
        }
        get productImageUrl () {
            const product = this.product;
            return `/web/image?model=product.product&field=image_128&id=${product.id}&write_date=${product.write_date}&unique=1`;
        }
        choose_products(e){
            var self = this;
            this.selected = [];
            this.counter = [];
            this.quantity = [];
            var $target = $(e.currentTarget);
            var combo = $target.data('combo-id');
            var category = $target.data('category-id');
            var product = $target.data('product-id');
            _.each(this.props.optional, function (category_option) {
                if (category_option['id'] === combo && category_option['category'] === category){
                    var selection_count = 0;
                    _.each(category_option.combo_products, function (combo_product) {
                        if (combo_product.selected){
                            selection_count += combo_product.counter;
                        }
                    });
                    _.each(category_option.combo_products, function (combo_product) {
                        if(combo_product['id'] === product){
                            combo_product['counter'] = parseInt($('.qty[data-product-id=' + product.toString() + ']').val())
                            combo_product['quantity'] = parseInt($('.qty[data-product-id=' + product.toString() + ']').val())
                            if (combo_product['selected'] && selection_count < category_option.limit){
                                
//                                $('.qty[data-product-id='+product.toString()+']').val(parseInt($('.qty[data-product-id='+product.toString()+']').val())+1);
//                                combo_product['counter'] = parseInt($('.qty[data-product-id=' + product.toString() + ']').val())
//                                $('.qty[data-product-id='+product.toString()+']').val(0);


                                combo_product['selected'] = false;
                                $target.find('.combo-select').hide();
                                $('.buttons_added[data-product-id='+product.toString()+']').hide();
//                                $target.find('.buttons_added').hide();
                                var index = self.selected.indexOf(combo_product);
                                if (index > -1) {
                                   self.selected.splice(index, 1);
                                }
                            }
                            else if (selection_count < category_option.limit){
                                combo_product['selected'] = true;
                                combo_product['counter'] = 0;
                                combo_product['quantity'] = 0;
                                $('.buttons_added[data-product-id='+product.toString()+']').show();
//                                $target.find('.buttons_added').show();
                                $target.find('.combo-select').text("Selected").show('fast');
                                self.selected.push(combo_product);
                            }
                            else{
//                            $('.qty[data-product-id='+product.toString()+']').val(parseInt($('.qty[data-product-id='+product.toString()+']').val())-1);
                                alert("Already selected enough options for this category");
                            }
                        }
                    });
                }
            });
        }
        plus_value(e){
            var self = this;
            this.selected = [];
            this.counter = [];
            this.quantity = [];
            var $target = $(e.currentTarget);
            var combo = $target.data('combo-id');
            var category = $target.data('category-id');
            var product = $target.data('product-id');
            
            _.each(this.props.optional, function (category_option) {
                if (category_option['id'] === combo && category_option['category'] === category){
                    var selection_count = 0;
                    
                    _.each(category_option.combo_products, function (combo_product) {
                        if (combo_product.selected){
                            selection_count += combo_product.counter;
                        }
                    });
                    _.each(category_option.combo_products, function (combo_product) {
                        if(combo_product['id'] === product){
                            if (combo_product['selected'] && selection_count < category_option.limit){
                                
                                $('.qty[data-product-id='+product.toString()+']').val(parseInt($('.qty[data-product-id='+product.toString()+']').val())+1);
                            combo_product['counter'] = parseInt($('.qty[data-product-id=' + product.toString() + ']').val())
                            combo_product['quantity'] = parseInt($('.qty[data-product-id=' + product.toString() + ']').val())
                                var index = self.selected.indexOf(combo_product);
                                if (index > -1) {
                                   self.selected.splice(index, 1);
                                }
                            } else{
                                alert("Already selected enough options for this category");
                            }
                        }
                    });
                }
            });
        }

        minus_value(e){
            var self = this;
            this.selected = [];
            this.counter = [];
            this.quantity = [];
            var $target = $(e.currentTarget);
            var combo = $target.data('combo-id');
            var category = $target.data('category-id');
            var product = $target.data('product-id');
            
            _.each(this.props.optional, function (category_option) {
                if (category_option['id'] === combo && category_option['category'] === category){
                    var selection_count = 0;
                    
                    _.each(category_option.combo_products, function (combo_product) {

                        if (combo_product.selected){

                            selection_count += combo_product.counter;
                        }
                    });
                    _.each(category_option.combo_products, function (combo_product) {
                        if(combo_product['id'] === product){
                        
                            $('.qty[data-product-id='+product.toString()+']').val(parseInt($('.qty[data-product-id='+product.toString()+']').val())-1);

                            combo_product['counter'] = parseInt($('.qty[data-product-id=' + product.toString() + ']').val())
                            combo_product['quantity'] = parseInt($('.qty[data-product-id=' + product.toString() + ']').val())

                        }
                    });
                }
            });
        }
        go_back_screen() {
            this.showScreen('ProductScreen');
            this.trigger('close-popup');
        }

        click_on_bag_product(event) {
            var self = this;
            var bag_id = parseInt(event.currentTarget.dataset['productId'])
            self.env.pos.get_order().add_product(self.env.pos.db.product_by_id[bag_id]);
            self.trigger('close-popup');
        }
    };
    ComboPopup.template = 'ComboPopup';
    Registries.Component.add(ComboPopup);
    return ComboPopup;
});
