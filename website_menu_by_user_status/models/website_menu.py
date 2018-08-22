import logging
_logger = logging.getLogger(__name__)
from openerp import models, fields
from openerp.tools.translate import _


class WebsiteMenu(models.Model):
    """Improve website.menu with adding booleans that drive
    if the menu is displayed when the user is logger or not.
    """
    _inherit = 'website.menu'

    user_logged = fields.Boolean(
        string="User Logged",
        default=True,
        help=_("If checked, "
               "the menu will be displayed when the user is logged.")
    )

    user_not_logged = fields.Boolean(
        string="User Not Logged",
        default=True,
        help=_("If checked, "
               "the menu will be displayed when the user is not logged.")
)