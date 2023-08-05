# Copyright (C) 2011 Julius Network Solutions SARL <contact@julius.fr>
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests import common


class TestsCommon(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.location_obj = cls.env["stock.location"]
        product_obj = cls.env["product.product"]
        cls.wizard_obj = cls.env["wiz.stock.move.location"]
        cls.quant_obj = cls.env["stock.quant"]
        cls.company = cls.env.ref("base.main_company")

        cls.internal_loc_1 = cls.location_obj.create(
            {
                "name": "INT_1",
                "usage": "internal",
                "active": True,
                "company_id": cls.company.id,
            }
        )
        cls.internal_loc_2 = cls.location_obj.create(
            {
                "name": "INT_2",
                "usage": "internal",
                "active": True,
                "company_id": cls.company.id,
            }
        )
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product_no_lots = product_obj.create(
            {"name": "Pineapple", "type": "product", "tracking": "none"}
        )
        cls.product_lots = product_obj.create(
            {"name": "Apple", "type": "product", "tracking": "lot"}
        )
        cls.lot1 = cls.env["stock.production.lot"].create(
            {
                "name": "lot1",
                "product_id": cls.product_lots.id,
                "company_id": cls.company.id,
            }
        )
        cls.lot2 = cls.env["stock.production.lot"].create(
            {
                "name": "lot2",
                "product_id": cls.product_lots.id,
                "company_id": cls.company.id,
            }
        )
        cls.lot3 = cls.env["stock.production.lot"].create(
            {
                "name": "lot3",
                "product_id": cls.product_lots.id,
                "company_id": cls.company.id,
            }
        )

    def setup_product_amounts(self):
        self.set_product_amount(self.product_no_lots, self.internal_loc_1, 123)
        self.set_product_amount(
            self.product_lots, self.internal_loc_1, 1.0, lot_id=self.lot1
        )
        self.set_product_amount(
            self.product_lots, self.internal_loc_1, 1.0, lot_id=self.lot2
        )
        self.set_product_amount(
            self.product_lots, self.internal_loc_1, 1.0, lot_id=self.lot3
        )

    def set_product_amount(self, product, location, amount, lot_id=None):
        self.env["stock.quant"]._update_available_quantity(
            product, location, amount, lot_id=lot_id
        )

    def check_product_amount(self, product, location, amount, lot_id=None):
        self.assertEqual(
            self.env["stock.quant"]._get_available_quantity(
                product, location, lot_id=lot_id
            ),
            amount,
        )

    def _create_wizard(self, origin_location, destination_location):
        move_location_wizard = self.env["wiz.stock.move.location"]
        return move_location_wizard.create(
            {
                "origin_location_id": origin_location.id,
                "destination_location_id": destination_location.id,
            }
        )
