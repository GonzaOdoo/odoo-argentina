import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Las account_account_tags ya no las usamos en 19 y por lo tanto las eliminamos
    ver  commit relacionado en https://github.com/ingadhoc/odoo-argentina/commit/63d2dd6eaab9cdadfb81a7f466d1c76d39aad7a9
    Pero para el caso de los clientes que migran donde ya estan usando esas etiquetas no
    las podemos borrar, por eso implementamos este script que elimina el XML ID de etiquetas
    en uso, asi quedan las etiquetas y evitamos se borren las account_account_tags que estan
    en uso"""
    env = api.Environment(cr, SUPERUSER_ID, {})

    xml_id_names = [
        "tag_a_cuenta_ganancias",
        "tag_a_cuenta_iva",
        "tag_iva_primer_parrafo",
        "tag_unaffected_earnings",
        "tag_impuestos_a_las_ganancias",
        "tag_liquidacion_de_iva",
        "tag_liquidacion_de_iibb",
        "tag_liquidacion_de_ganancias",
        "tag_liquidacion_sicore_aplicado",
        "tag_liquidacion_iibb_aplicado",
        "tax_tag_a_cuenta_suss",
        "tax_tag_a_cuenta_iibb",
        "tax_tag_a_cuenta_ganancias",
        "tax_tag_a_cuenta_iva",
        "tag_ret_perc_iibb_aplicada",
        "tag_ret_perc_sicore_aplicada",
        "tag_tax_jurisdiccion_901",
        "tag_tax_jurisdiccion_902",
        "tag_tax_jurisdiccion_903",
        "tag_tax_jurisdiccion_904",
        "tag_tax_jurisdiccion_911",
        "tag_tax_jurisdiccion_912",
        "tag_tax_jurisdiccion_913",
        "tag_tax_jurisdiccion_914",
        "tag_tax_jurisdiccion_915",
        "tag_tax_jurisdiccion_916",
        "tag_tax_jurisdiccion_917",
        "tag_tax_jurisdiccion_918",
        "tag_tax_jurisdiccion_919",
        "tag_tax_jurisdiccion_920",
        "tag_tax_jurisdiccion_921",
        "tag_tax_jurisdiccion_922",
        "tag_tax_jurisdiccion_923",
        "tag_tax_jurisdiccion_924",
    ]
    for xml_id_name in xml_id_names:
        account_tag_id = env.ref(f"l10n_ar_ux.{xml_id_name}", raise_if_not_found=False)
        if account_tag_id:
            cr.execute(
                """
                SELECT 1
                FROM account_account_tag_account_tax_repartition_line_rel
                WHERE account_account_tag_id = %s
                LIMIT 1
            """,
                (account_tag_id.id,),
            )
            used_in_taxes = cr.fetchone()
            if used_in_taxes:
                _logger.info(f"Eliminamos el extenal ref l10n_ar_ux.{xml_id_name} ya que se encuentra en uso")
                cr.execute(
                    """
                    DELETE FROM ir_model_data
                    WHERE module = 'l10n_ar_ux' AND name = %s
                """,
                    (xml_id_name,),
                )
    
    cr.execute("""
        SELECT id, payment_date, create_date
        FROM l10n_latam_check
        WHERE id = 1400
    """)
    _logger.warning("Check data: %s", cr.fetchall())
    cr.execute("""
        UPDATE l10n_latam_check
           SET payment_date = '2026-05-07'
         WHERE id = 1400
           AND payment_date IS NULL
    """)
    _logger.warning("Rows updated: %s", cr.rowcount)
    _logger.warning("Set payment_date to create_date for l10n_latam_check with id 1400")
    # Corregimos campo Studio que en v19 pasa a requerido
    cr.execute("""
        UPDATE sale_order
        SET x_studio_stockcliente = 'Cliente'
        WHERE id = 1127
        AND x_studio_stockcliente IS NULL
    """)
    _logger.warning(
        "Fixed x_studio_stockcliente on sale_order 1127"
    )

    cr.execute("""
        SELECT id, x_studio_stockcliente
        FROM sale_order
        WHERE id = 1127
    """)
    _logger.warning(
        "Sale order after update: %s",
        cr.fetchall()
    )