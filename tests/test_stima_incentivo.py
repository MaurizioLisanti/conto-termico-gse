"""Tests for _stima_incentivo pure function."""
import pytest
from tools import _stima_incentivo, _get_tariffe


# ── pompa di calore ────────────────────────────────────────────────────────────

def test_pdc_privato_10kw():
    r = _stima_incentivo("pompa di calore", potenza_kw=10.0)
    assert r["incentivo_annuo_eur"] == pytest.approx(1100.0)
    assert r["incentivo_totale_eur"] == pytest.approx(5500.0)
    assert r["durata_anni"] == 5


def test_pdc_pa_10kw():
    r = _stima_incentivo("pompa di calore", potenza_kw=10.0, tipo_soggetto="PA")
    assert r["incentivo_annuo_eur"] == pytest.approx(110 * 10 * 1.15)
    assert r["incentivo_totale_eur"] == pytest.approx(110 * 10 * 1.15 * 5)


def test_pdc_pa_case_insensitive():
    r = _stima_incentivo("pompa di calore", potenza_kw=10.0, tipo_soggetto="pa")
    assert r["incentivo_annuo_eur"] == pytest.approx(110 * 10 * 1.15)


def test_pdc_senza_potenza_restituisce_nota():
    r = _stima_incentivo("pompa di calore")
    assert "nota" in r
    assert "incentivo_annuo_eur" not in r


# ── solare termico ─────────────────────────────────────────────────────────────

def test_solare_5mq_privato():
    r = _stima_incentivo("solare termico", superficie_mq=5.0)
    assert r["incentivo_annuo_eur"] == pytest.approx(245 * 5)
    assert r["incentivo_totale_eur"] == pytest.approx(245 * 5 * 5)
    assert r["durata_anni"] == 5


def test_solare_pa_moltiplicatore():
    r = _stima_incentivo("solare termico", superficie_mq=5.0, tipo_soggetto="PA")
    assert r["incentivo_annuo_eur"] == pytest.approx(245 * 5 * 1.15)


def test_solare_senza_superficie_restituisce_nota():
    r = _stima_incentivo("solare termico")
    assert "nota" in r


# ── biomassa ───────────────────────────────────────────────────────────────────

def test_biomassa_20kw():
    r = _stima_incentivo("biomassa", potenza_kw=20.0)
    assert r["incentivo_annuo_eur"] == pytest.approx(95 * 20)
    assert r["incentivo_totale_eur"] == pytest.approx(95 * 20 * 5)
    assert r["durata_anni"] == 5


# ── caldaia a condensazione ────────────────────────────────────────────────────

def test_condensazione_15kw():
    r = _stima_incentivo("caldaia condensazione", potenza_kw=15.0)
    assert r["incentivo_annuo_eur"] == pytest.approx(65 * 15)
    assert r["incentivo_totale_eur"] == pytest.approx(65 * 15 * 2)
    assert r["durata_anni"] == 2


# ── scaldacqua pompa di calore ─────────────────────────────────────────────────

def test_scaldacqua_senza_potenza_restituisce_nota():
    # "scaldacqua pompa di calore" contains "pompa di calore" → matches that tariff first.
    # Without potenza_kw the result contains "nota" rather than an incentivo_annuo_eur.
    r = _stima_incentivo("scaldacqua pompa di calore")
    assert "nota" in r
    assert "incentivo_annuo_eur" not in r


def test_scaldacqua_con_potenza_usa_tariffa_pdc():
    # Falls into the "pompa di calore" tariff (110 €/kW/anno, 5 anni).
    r = _stima_incentivo("scaldacqua pompa di calore", potenza_kw=3.0)
    assert r["incentivo_annuo_eur"] == pytest.approx(110 * 3.0)
    assert r["durata_anni"] == 5


# ── avvertenza sempre presente ─────────────────────────────────────────────────

def test_avvertenza_sempre_presente():
    r = _stima_incentivo("pompa di calore", potenza_kw=10.0)
    assert "avvertenza" in r
    assert "GSE" in r["avvertenza"]


# ── tipo non riconosciuto → ValueError ────────────────────────────────────────

def test_tipo_sconosciuto_raise():
    with pytest.raises(ValueError, match="non riconosciuto"):
        _stima_incentivo("pannello fotovoltaico")


def test_tipo_vuoto_raise():
    with pytest.raises(ValueError):
        _stima_incentivo("")


# ── _get_tariffe fallback ──────────────────────────────────────────────────────

def test_get_tariffe_fallback_senza_client():
    """_get_tariffe() con client=None ritorna il dizionario hardcoded completo."""
    t = _get_tariffe()
    assert "pompa di calore" in t
    assert "solare termico" in t
    assert "biomassa" in t
    assert "caldaia condensazione" in t
    assert t["pompa di calore"]["tariffa_base_kwh"] == 110
    assert t["solare termico"]["tariffa_base_mq"] == 245


def test_stima_incentivo_client_manager_none_usa_fallback():
    """_stima_incentivo con client_manager=None usa le tariffe hardcoded."""
    r = _stima_incentivo("pompa di calore", potenza_kw=10.0, client_manager=None)
    assert r["incentivo_annuo_eur"] == pytest.approx(1100.0)
    assert r["incentivo_totale_eur"] == pytest.approx(5500.0)
