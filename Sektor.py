# sectors = ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
#                 "Industrials", "Infrastructures", "Properties & Real Estate", "Technology", "Transportation & Logistic"]

from enum import Enum

class Sektor(Enum):
    ALL = "ALL SEKTOR"
    BasicMaterial = "BASIC MATERIALS"
    ConsumerCyclicals = "CONSUMER CYCLICALS"
    ConsumerNonCyclicals = "CONSUMER NON-CYCLICALS"
    Energy = "ENERGY"
    Financials = "FINANCIALS"
    Healthcare = "HEALTHCARE"
    Industrials = "INDUSTRIALS"
    Infrastructures = "INFRASTUCTURES"
    PropertiesRealEstate = "PROPERTIES & REAL ESTATE"
    Technology = "TECHNOLOGY"
    TransportationLogistic = "TRANSPORTATION & LOGISTIC"