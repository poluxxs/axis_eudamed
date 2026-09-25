import xml.etree.ElementTree as ET
import re

def create_udidata_xml(
    risk_class,
    model,
    name,
    primary_DI,
    manufacturer_code,
    authorisedRepresentative_code,
    basic_UDIDI,
    reference,
    trade_name,
    description,
    mdn_code,
    sterilization,
    number_of_reuses,
    reusable,
    diameter,
    length,
    #packaging_DI,
    number_of_items,
    start_date="2020-02-01+01:00"
):
    # Correct errors within primary DI
    if not basic_UDIDI.startswith("076"):
        basic_UDIDI = "0" + basic_UDIDI

    #for compliance assure that there is no space and that there is a . not a , in the numbers
    diameter = re.sub(r"\s+", "", str(diameter)).replace(",", ".")
    length = re.sub(r"\s+", "", str(length)).replace(",", ".")

    UDIDIData = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/v1"
    XSI = "http://www.w3.org/2001/XMLSchema-instance"
    Udidi = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/UDIDI/v1"
    Commondi = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/CommonDevice/v1"
    Marketinfo = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/MktInfo/MarketInfo/v1"
    Lsn ="https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Common/LanguageSpecific/v1"

    udidiDatas = ET.Element(
    f"{{{UDIDIData}}}UDIDIData",
    {f"{{{XSI}}}type": "udidiDatas:MDRUDIDIDataType"}
    )

    # -------------------------
    # MDRUDIDIData
    # -------------------------

    identifier2 = ET.SubElement(udidiDatas, f"{{{Udidi}}}identifier")
    ET.SubElement(identifier2, f"{{{Commondi}}}DICode").text = basic_UDIDI
    ET.SubElement(identifier2, f"{{{Commondi}}}issuingEntityCode").text = "GS1"

    status = ET.SubElement(udidiDatas, f"{{{Udidi}}}status")
    ET.SubElement(status, f"{{{Commondi}}}code").text = "ON_THE_MARKET"

    desc = ET.SubElement(udidiDatas, f"{{{Udidi}}}additionalDescription")
    name_block = ET.SubElement(desc, f"{{{Lsn}}}name")

    ET.SubElement(name_block, f"{{{Lsn}}}language").text = "EN"
    ET.SubElement(name_block, f"{{{Lsn}}}textValue").text = description

    basicUDI = ET.SubElement(udidiDatas, f"{{{Udidi}}}basicUDIIdentifier")
    ET.SubElement(basicUDI, f"{{{Commondi}}}DICode").text = primary_DI
    ET.SubElement(basicUDI, f"{{{Commondi}}}issuingEntityCode").text = "GS1"

    ET.SubElement(udidiDatas, f"{{{Udidi}}}MDNCodes").text = mdn_code
    ET.SubElement(udidiDatas, f"{{{Udidi}}}productionIdentifier").text = "BATCH_NUMBER MANUFACTURING_DATE"
    ET.SubElement(udidiDatas, f"{{{Udidi}}}referenceNumber").text = reference
    ET.SubElement(udidiDatas, f"{{{Udidi}}}sterile").text = "false"
    ET.SubElement(udidiDatas, f"{{{Udidi}}}sterilization").text = sterilization

    trade = ET.SubElement(udidiDatas, f"{{{Udidi}}}tradeNames")
    trade_name_block = ET.SubElement(trade, f"{{{Lsn}}}name")

    #packages = ET.SubElement(udidiDatas, f"{{{Udidi}}}packages")
    #package = ET.SubElement(packages, f"{{{Udidi}}}package")

    # identifier
    #identifier = ET.SubElement(package, f"{{{Udidi}}}identifier")
    #ET.SubElement(identifier, f"{{{Commondi}}}DICode").text = packaging_DI
    #ET.SubElement(identifier, f"{{{Commondi}}}issuingEntityCode").text = "GS1"

    # status
    #status = ET.SubElement(package, f"{{{Udidi}}}status")
    #ET.SubElement(status, f"{{{Commondi}}}code").text = "ON_THE_MARKET"

    # child
    #child = ET.SubElement(package, f"{{{Udidi}}}child")
    #ET.SubElement(child, f"{{{Commondi}}}DICode").text = primary_DI
    #ET.SubElement(child, f"{{{Commondi}}}issuingEntityCode").text = "GS1"

    # number of items
    #ET.SubElement(package, f"{{{Udidi}}}numberOfItems").text = number_of_items

    ET.SubElement(trade_name_block, f"{{{Lsn}}}language").text = "EN"
    ET.SubElement(trade_name_block, f"{{{Lsn}}}textValue").text = trade_name

    ET.SubElement(
        udidiDatas,
        f"{{{Udidi}}}numberOfReuses"
    ).text = str(number_of_reuses)

    # -------------------------
    # Market Infos
    # -------------------------
    market_infos = ET.SubElement(
        udidiDatas,
        f"{{{Udidi}}}marketInfos"
    )

    countries = [
        "AT","BE","BG","HR","CY","CZ","DK",
        "EE","FI","FR","DE","EL","HU","IS",
        "IE","IT","LV","LI","LT","LU","MT",
        "PT","NL","NO","PL","RO","SK","SI",
        "ES","SE","TR","XI"
    ]

    for c in countries:

        mi = ET.SubElement(
            market_infos,
            f"{{{Marketinfo}}}marketInfo"
        )

        ET.SubElement(
            mi,
            f"{{{Marketinfo}}}country"
        ).text = c

        ET.SubElement(
            mi,
            f"{{{Marketinfo}}}originalPlacedOnTheMarket"
        ).text = "true" if c == "FR" else "false"

        ET.SubElement(
            mi,
            f"{{{Marketinfo}}}startDate"
        ).text = start_date
    ET.SubElement(udidiDatas, f"{{{Udidi}}}baseQuantity").text = number_of_items
    ET.SubElement(udidiDatas, f"{{{Udidi}}}latex").text = "false"
    ET.SubElement(udidiDatas, f"{{{Udidi}}}reprocessed").text = "false"

    clinical_sizes = ET.SubElement(udidiDatas, f"{{{Udidi}}}clinicalSizes")

    # -------------------
    # Diameter
    # -------------------
    cs1 = ET.SubElement(
        clinical_sizes,
        f"{{{Commondi}}}clinicalSize",
        {f"{{{XSI}}}type": "commondi:ValueClinicalSizeType"}
    )

    ET.SubElement(cs1, f"{{{Commondi}}}clinicalSizeType").text = "CST9"
    ET.SubElement(cs1, f"{{{Commondi}}}value").text = str(diameter)
    ET.SubElement(cs1, f"{{{Commondi}}}valueUnit").text = "MU50"

    # -------------------
    # Length
    # -------------------
    cs2 = ET.SubElement(
        clinical_sizes,
        f"{{{Commondi}}}clinicalSize",
        {f"{{{XSI}}}type": "commondi:ValueClinicalSizeType"}
    )

    ET.SubElement(cs2, f"{{{Commondi}}}clinicalSizeType").text = "CST19"
    ET.SubElement(cs2, f"{{{Commondi}}}value").text = str(length)
    ET.SubElement(cs2, f"{{{Commondi}}}valueUnit").text = "MU50"

    return udidiDatas