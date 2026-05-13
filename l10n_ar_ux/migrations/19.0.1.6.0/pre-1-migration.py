from odoo.upgrade import util
import logging

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    _logger.info("Mergeamos l10n_ar_account_withholding y l10n_ar_withholding_ux en l10n_ar_tax")
    util.merge_module(
        cr,
        "l10n_ar_account_withholding",
        "l10n_ar_tax",
    )

    util.merge_module(
        cr,
        "l10n_ar_withholding_ux",
        "l10n_ar_tax",
    )