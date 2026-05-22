"""Tests for _verifica_ammissibilita pure function."""
import pytest
from tools import _verifica_ammissibilita


# ── pompa di calore ────────────────────────────────────────────────────────────

def test_pdc_cop_valido_zona_e():
    r = _verifica_ammissibilita("pompa di calore aria-acqua", cop_certificato=3.2, zona_climatica="E")
    assert r["ammissibile"] is True
    assert "3.2" in r["motivazione"]
    assert r["tipo_intervento_ct"] == "B.2 - Pompe di calore per climatizzazione invernale"


def test_pdc_cop_insufficiente_zona_e():
    r = _verifica_ammissibilita("pompa di calore aria-acqua", cop_certificato=2.5, zona_climatica="E")
    assert r["ammissibile"] is False
    assert "Non ammissibile" in r["motivazione"]


def test_pdc_cop_esatto_soglia_zona_c():
    # COP esattamente pari alla soglia → ammissibile
    r = _verifica_ammissibilita("pompa di calore", cop_certificato=2.8, zona_climatica="C")
    assert r["ammissibile"] is True


def test_pdc_potenza_oltre_limite():
    r = _verifica_ammissibilita("pompa di calore", potenza_kw=2500.0, cop_certificato=4.0, zona_climatica="D")
    assert r["ammissibile"] is False
    assert "2.000 kW" in r["motivazione"] or "2500" in r["motivazione"]


def test_pdc_senza_cop_e_zona():
    r = _verifica_ammissibilita("pompa di calore")
    assert r["ammissibile"] is True
    assert "requisiti_mancanti" in r
    assert len(r["requisiti_mancanti"]) > 0


def test_pdc_con_certificazione_valida():
    r = _verifica_ammissibilita("pompa di calore", certificazioni=["EN 14511 test"])
    assert r["ammissibile"] is True
    assert r["requisiti_mancanti"] == []


def test_heat_pump_keyword():
    r = _verifica_ammissibilita("heat pump 12 kW")
    assert r["tipo_intervento_ct"] == "B.2 - Pompe di calore per climatizzazione invernale"


# ── solare termico ─────────────────────────────────────────────────────────────

def test_solare_superficie_sufficiente():
    r = _verifica_ammissibilita("solare termico", superficie_mq=5.0)
    assert r["ammissibile"] is True
    assert r["tipo_intervento_ct"] == "B.4 - Collettori solari termici"


def test_solare_superficie_minima_esatta():
    # esattamente 1.5 m² non è < 1.5, quindi ammissibile
    r = _verifica_ammissibilita("solare termico", superficie_mq=1.5)
    assert r["ammissibile"] is True


def test_solare_superficie_insufficiente():
    r = _verifica_ammissibilita("solare termico", superficie_mq=1.0)
    assert r["ammissibile"] is False
    assert "1,5 m²" in r["motivazione"]


def test_solare_con_solar_keymark():
    r = _verifica_ammissibilita("solare termico", certificazioni=["Solar Keymark EU"])
    assert r["ammissibile"] is True
    assert r["requisiti_mancanti"] == []


def test_solare_senza_certificazione():
    r = _verifica_ammissibilita("solare termico")
    assert "Solar Keymark" in r["requisiti_mancanti"][0]


# ── biomassa / pellet ──────────────────────────────────────────────────────────

def test_biomassa_ammissibile():
    r = _verifica_ammissibilita("caldaia biomassa")
    assert r["ammissibile"] is True
    assert r["tipo_intervento_ct"] == "B.5 - Generatori di calore a biomassa"
    assert r["durata_incentivo"] == "5 anni"


def test_pellet_ammissibile():
    r = _verifica_ammissibilita("stufa a pellet")
    assert r["ammissibile"] is True
    assert "EN 303-5" in r["requisiti_mancanti"][0]


def test_legna_ammissibile():
    r = _verifica_ammissibilita("caminetto a legna")
    assert r["ammissibile"] is True


# ── caldaia a gas ──────────────────────────────────────────────────────────────

def test_gas_non_condensazione_non_ammissibile():
    r = _verifica_ammissibilita("caldaia a gas")
    assert r["ammissibile"] is False


def test_caldaia_condensazione_ammissibile():
    r = _verifica_ammissibilita("caldaia a condensazione")
    assert r["ammissibile"] is True
    assert r["tipo_intervento_ct"] == "B.1 - Sostituzione con caldaie a condensazione"
    assert r["durata_incentivo"] == "2 anni"


# ── scaldacqua / ACS ──────────────────────────────────────────────────────────

def test_scaldacqua_ammissibile():
    # "scaldacqua" alone avoids the "pompa di calore" branch
    r = _verifica_ammissibilita("scaldacqua")
    assert r["ammissibile"] is True
    assert r["tipo_intervento_ct"] == "B.3 - Scaldacqua a pompa di calore"
    assert r["durata_incentivo"] == "2 anni"


def test_acs_ammissibile():
    r = _verifica_ammissibilita("sistema ACS")
    assert r["ammissibile"] is True


# ── tipo non riconosciuto ──────────────────────────────────────────────────────

def test_tipo_sconosciuto():
    r = _verifica_ammissibilita("pannello fotovoltaico")
    assert r["ammissibile"] is None
    assert "non riconosciuto" in r["motivazione"]
